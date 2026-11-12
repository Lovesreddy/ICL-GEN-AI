import importlib
from types import SimpleNamespace

import httpx
import pytest
from fastapi.testclient import TestClient


def build_client(tmp_path, monkeypatch):
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{tmp_path / 'organic_farming.db'}")
    monkeypatch.setenv("VECTOR_DIR", str(tmp_path / "vector_store"))
    monkeypatch.setenv("KNOWLEDGE_DIR", str(tmp_path / "knowledge_base"))
    monkeypatch.setenv("AUTO_INDEX", "false")
    monkeypatch.setenv("EMBEDDING_BACKEND", "deterministic")
    monkeypatch.setenv("LLM_PROVIDER", "groq")
    monkeypatch.setenv("GROQ_API_KEY", "")
    monkeypatch.setenv("JWT_SECRET", "test-secret-key-that-is-long-enough-123")
    monkeypatch.setenv("ADMIN_EMAIL", "admin@example.com")
    monkeypatch.setenv("ADMIN_PASSWORD", "adminpass123")
    monkeypatch.setenv("ADMIN_NAME", "Farm Admin")

    import app.config
    import app.database
    import app.main
    from app.services.seed import seed_admin, seed_crops

    app.config.get_settings.cache_clear()
    importlib.reload(app.config)
    importlib.reload(app.database)
    importlib.reload(app.main)

    db = app.database.SessionLocal()
    try:
        app.main.init_database()
        seed_admin(db)
        seed_crops(db)
    finally:
        db.close()

    return TestClient(app.main.app)


def test_health_and_crops(tmp_path, monkeypatch):
    client = build_client(tmp_path, monkeypatch)

    health = client.get("/api/health")
    assert health.status_code == 200
    assert health.json()["database"] in {"ok", "degraded"}
    assert health.json()["nlp"]["lemmatizer"] == "identity"

    crops = client.get("/api/crops")
    assert crops.status_code == 200
    payload = crops.json()
    assert payload and any(item["crop_name"] for item in payload)
    assert len(payload) >= 18


def test_nlp_fallback_preserves_negation_without_external_corpora():
    from app.services.nlp_service import analyze

    result = analyze("Tomatoes should not be watered with contaminated water.")

    assert result["lemmatizer"] == "identity"
    assert "not" in result["tokens_without_stopwords"]


def test_pdf_upload_requires_optional_document_dependencies(tmp_path, monkeypatch):
    build_client(tmp_path, monkeypatch)
    from app.services import ingestion

    monkeypatch.setattr(ingestion.importlib.util, "find_spec", lambda _name: None)
    with pytest.raises(ingestion.ExtractionError, match="PDF uploads are unavailable"):
        ingestion.validate_upload("guide.pdf", 16, "general")


def test_vite_fallback_port_is_allowed_by_cors(tmp_path, monkeypatch):
    client = build_client(tmp_path, monkeypatch)

    for origin in ("http://localhost:5175", "http://127.0.0.1:5175"):
        response = client.options(
            "/api/crops",
            headers={"Origin": origin, "Access-Control-Request-Method": "GET"},
        )
        assert response.status_code == 200
        assert response.headers["access-control-allow-origin"] == origin


def test_signed_in_farmer_can_add_a_shared_crop(tmp_path, monkeypatch):
    client = build_client(tmp_path, monkeypatch)
    crop = {
        "crop_name": "Chickpea",
        "soil_type": "Loam and sandy loam",
        "season": "Rabi",
        "description": "A cool-season pulse crop with low water requirements.",
        "climate": "Cool and dry",
        "water_need": "Low",
        "suitable_soil": "Well-drained loam with no prolonged waterlogging.",
        "sowing_season": "Sow in the locally recommended cool-season window.",
        "organic_fertilizers": "Use mature compost and avoid excessive nitrogen.",
        "irrigation": "Protect flowering and pod formation from moisture stress.",
        "pest_management": "Rotate crops and scout for aphids and pod borers.",
        "harvesting": "Harvest when most pods are mature and dry the seed before storage.",
    }

    assert client.post("/api/crops", json=crop).status_code == 401
    registration = client.post(
        "/api/auth/register",
        json={"name": "Farmer Two", "email": "farmer2@example.com", "password": "secret123"},
    )
    token = registration.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    created = client.post("/api/crops", json=crop, headers=headers)
    assert created.status_code == 201
    assert created.json()["crop_name"] == "Chickpea"
    assert any(item["crop_name"] == "Chickpea" for item in client.get("/api/crops").json())
    assert client.post("/api/crops", json=crop, headers=headers).status_code == 409


def test_seeding_adds_missing_profiles_without_removing_user_crops(tmp_path, monkeypatch):
    client = build_client(tmp_path, monkeypatch)
    import app.database
    from app.models import CropInformation
    from app.services.seed import seed_crops

    db = app.database.SessionLocal()
    try:
        db.add(
            CropInformation(
                crop_name="Farmer's crop",
                soil_type="loam",
                season="local",
                description="A user-added crop profile.",
                cultivation_details=(
                    '{"suitable_soil":"loam","sowing_season":"local season",'
                    '"organic_fertilizers":"mature compost","irrigation":"moderate water",'
                    '"pest_management":"scout regularly","harvesting":"harvest when mature"}'
                ),
                climate="local",
                water_need="medium",
            )
        )
        maize = db.query(CropInformation).filter_by(crop_name="Maize").one()
        db.delete(maize)
        db.commit()

        seed_crops(db)
        names = {row.crop_name for row in db.query(CropInformation).all()}
        assert "Maize" in names
        assert "Farmer's crop" in names
        assert len(names) == 19

        seed_crops(db)
        assert db.query(CropInformation).count() == 19
    finally:
        db.close()
    assert client.get("/api/crops").status_code == 200


def test_knowledge_hub_articles_are_searchable_and_openable(tmp_path, monkeypatch):
    client = build_client(tmp_path, monkeypatch)

    articles = client.get("/api/knowledge").json()
    assert len(articles) >= 13
    assert any(article["id"] == "seed-selection-and-nursery" for article in articles)
    soil_search = client.get("/api/knowledge", params={"q": "India"}).json()
    assert any(article["id"] == "soil-types-india" for article in soil_search)
    search = client.get("/api/knowledge", params={"q": "seed"}).json()
    assert any(article["id"] == "seed-selection-and-nursery" for article in search)
    detail = client.get("/api/knowledge/soil-types-india")
    assert detail.status_code == 200
    assert "Alluvial soils" in detail.json()["description"]
    assert "Black (regur)" in detail.json()["description"]

    from app.services.seed import write_sample_files

    sample_path, title, category = next(
        item for item in write_sample_files() if item[1] == "Major soil groups in India"
    )
    assert title == "Major soil groups in India"
    assert category == "soil"
    assert "Peaty and marshy soils" in sample_path.read_text(encoding="utf-8")


def test_register_login_and_me(tmp_path, monkeypatch):
    client = build_client(tmp_path, monkeypatch)

    response = client.post(
        "/api/auth/register",
        json={"name": "Farmer One", "email": "farmer@example.com", "password": "secret123"},
    )
    assert response.status_code == 201
    payload = response.json()
    token = payload["access_token"]
    assert token

    me = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me.status_code == 200
    assert me.json()["email"] == "farmer@example.com"

    login = client.post(
        "/api/auth/login",
        json={"email": "farmer@example.com", "password": "secret123"},
    )
    assert login.status_code == 200
    assert login.json()["user"]["email"] == "farmer@example.com"


def test_seeded_admin_can_login(tmp_path, monkeypatch):
    client = build_client(tmp_path, monkeypatch)

    response = client.post(
        "/api/auth/login",
        json={"email": "admin@example.com", "password": "adminpass123"},
    )

    assert response.status_code == 200
    assert response.json()["user"]["role"] == "administrator"


def test_chat_without_documents_returns_graceful_status(tmp_path, monkeypatch):
    client = build_client(tmp_path, monkeypatch)

    response = client.post(
        "/api/chat/ask",
        json={"question": "How do I prepare compost?"},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["llm_status"] in {"no_context", "not_configured", "refused"}
    assert isinstance(payload["sources"], list)


def test_chat_uses_general_farming_knowledge_when_no_source_matches(monkeypatch):
    from app.services import rag

    question = "What are the soil types in India?"
    analysis = {
        "cleaned": question,
        "keywords": ["soil", "types", "India"],
        "intent": "soil_management",
        "confidence": 1.0,
        "normalized_query": "soil types india",
    }
    captured = {}
    monkeypatch.setattr(rag, "analyze", lambda _question: analysis)
    monkeypatch.setattr(rag, "retrieve", lambda _db, _question, _analysis: [])
    monkeypatch.setattr(rag, "get_settings", lambda: SimpleNamespace(llm_configured=True))
    monkeypatch.setattr(
        rag,
        "generate",
        lambda messages: captured.update({"messages": messages})
        or '{"answer":"India has several broad soil groups.","follow_ups":[],"used_source_indexes":[]}',
    )

    result = rag.answer_question(None, question)

    assert result["llm_status"] == "general_answer"
    assert result["sources"] == []
    assert "broad soil groups" in result["answer"]
    assert "well-established general agricultural knowledge" in captured["messages"][0]["content"]
    assert "No relevant indexed agricultural excerpts were found." in captured["messages"][1]["content"]


def test_photo_guide_accepts_consented_image_without_authentication(tmp_path, monkeypatch):
    client = build_client(tmp_path, monkeypatch)
    from app.routers import photo_guide

    captured = {}
    monkeypatch.setattr(
        photo_guide,
        "get_settings",
        lambda: SimpleNamespace(groq_api_key="test-key", groq_vision_model="qwen/qwen3.8-27b"),
    )
    monkeypatch.setattr(
        photo_guide,
        "analyze_image",
        lambda image, content_type, prompt: captured.update(
            image=image, content_type=content_type, prompt=prompt
        ) or "The image shows a tomato leaf; its cause cannot be confirmed from the photo alone.",
    )

    response = client.post(
        "/api/photo-guide/analyze",
        files={"image": ("leaf.jpg", b"\xff\xd8\xffsample", "image/jpeg")},
        data={
            "crop_name": "Tomato",
            "subject_type": "crop",
            "notes": "Some leaves have spots.",
            "consent_to_provider": "true",
        },
    )

    assert response.status_code == 200
    assert response.json()["model"] == "qwen/qwen3.8-27b"
    assert "cannot be confirmed" in response.json()["answer"]
    assert captured["image"] == b"\xff\xd8\xffsample"
    assert captured["content_type"] == "image/jpeg"
    assert "Some leaves have spots." in captured["prompt"]


def test_photo_guide_requires_provider_consent_and_real_image_signature(tmp_path, monkeypatch):
    client = build_client(tmp_path, monkeypatch)
    from app.routers import photo_guide

    monkeypatch.setattr(
        photo_guide,
        "get_settings",
        lambda: SimpleNamespace(groq_api_key="test-key", groq_vision_model="qwen/qwen3.8-27b"),
    )
    monkeypatch.setattr(photo_guide, "analyze_image", lambda *_args: "Should not be called.")

    missing_consent = client.post(
        "/api/photo-guide/analyze",
        files={"image": ("leaf.jpg", b"\xff\xd8\xffsample", "image/jpeg")},
        data={"crop_name": "Tomato", "subject_type": "crop"},
    )
    invalid_image = client.post(
        "/api/photo-guide/analyze",
        files={"image": ("leaf.jpg", b"not an image", "image/jpeg")},
        data={
            "crop_name": "Tomato",
            "subject_type": "crop",
            "consent_to_provider": "true",
        },
    )

    assert missing_consent.status_code == 400
    assert invalid_image.status_code == 415


def test_photo_guide_reports_missing_groq_key_without_calling_provider(tmp_path, monkeypatch):
    client = build_client(tmp_path, monkeypatch)
    from app.routers import photo_guide

    monkeypatch.setattr(
        photo_guide,
        "get_settings",
        lambda: SimpleNamespace(groq_api_key=None, groq_vision_model="qwen/qwen3.8-27b"),
    )
    monkeypatch.setattr(
        photo_guide,
        "analyze_image",
        lambda *_args: pytest.fail("The provider should not be called without a configured key."),
    )

    response = client.post(
        "/api/photo-guide/analyze",
        files={"image": ("leaf.jpg", b"\xff\xd8\xffsample", "image/jpeg")},
        data={
            "crop_name": "Tomato",
            "subject_type": "crop",
            "consent_to_provider": "true",
        },
    )

    assert response.status_code == 503
    assert "GROQ_API_KEY" in response.json()["detail"]


def test_photo_guide_limits_public_provider_usage(tmp_path, monkeypatch):
    client = build_client(tmp_path, monkeypatch)
    from app.routers import photo_guide

    photo_guide._analysis_requests.clear()
    monkeypatch.setattr(
        photo_guide,
        "get_settings",
        lambda: SimpleNamespace(groq_api_key="test-key", groq_vision_model="qwen/qwen3.8-27b"),
    )
    monkeypatch.setattr(photo_guide, "analyze_image", lambda *_args: "A cautious observation.")
    payload = {
        "files": {"image": ("leaf.jpg", b"\xff\xd8\xffsample", "image/jpeg")},
        "data": {
            "crop_name": "Tomato",
            "subject_type": "crop",
            "consent_to_provider": "true",
        },
    }

    responses = [client.post("/api/photo-guide/analyze", **payload) for _ in range(9)]

    assert [response.status_code for response in responses[:8]] == [200] * 8
    assert responses[8].status_code == 429


def test_groq_vision_sends_image_as_inline_data_url(monkeypatch):
    from app.services import llm

    captured = {}

    def fake_request(method, url, **kwargs):
        captured.update(method=method, url=url, **kwargs)
        return httpx.Response(
            200,
            json={"choices": [{"message": {"content": "Observed crop details."}}]},
            request=httpx.Request(method, url),
        )

    monkeypatch.setattr(llm, "_request_with_retries", fake_request)

    answer = llm._groq_vision(b"\xff\xd8\xff", "image/jpeg", "Check this leaf.", "test-key", "qwen/test")

    assert answer == "Observed crop details."
    assert captured["json"]["model"] == "qwen/test"
    user_content = captured["json"]["messages"][1]["content"]
    assert user_content[0]["text"] == "Check this leaf."
    assert user_content[1]["image_url"]["url"].startswith("data:image/jpeg;base64,")


def test_chat_intent_uses_word_boundaries_and_favors_specific_topics():
    from app.services.nlp_service import classify_intent

    assert classify_intent("How do I control aphids on tomato plants?")[0] == "pest_management"
    assert classify_intent("How do I check soil pH?")[0] == "soil_management"


def test_grok_settings_are_supported(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "grok")
    monkeypatch.setenv("GROK_API_KEY", "test-key")
    monkeypatch.setenv("GROK_MODEL", "grok-4.7")

    import app.config

    app.config.get_settings.cache_clear()
    settings = app.config.get_settings()

    assert settings.llm_provider == "grok"
    assert settings.xai_api_key == "test-key"
    assert settings.xai_model == "grok-4.7"
    assert settings.llm_configured is True


def test_xai_auth_error_names_the_config_setting_without_exposing_key(monkeypatch):
    from app.services import llm

    def reject_request(method, url, **_kwargs):
        return httpx.Response(401, request=httpx.Request(method, url))

    monkeypatch.setattr(llm.httpx, "request", reject_request)

    with pytest.raises(llm.LlmError, match="xAI rejected.*GROK_API_KEY"):
        llm._xai([{"role": "user", "content": "test"}], "test-secret", "grok-4.7")


def test_xai_uses_responses_api_and_extracts_answer_text(monkeypatch):
    from app.services import llm

    captured = {}

    def fake_request(method, url, **kwargs):
        captured.update(method=method, url=url, **kwargs)
        return httpx.Response(
            200,
            json={
                "output": [
                    {
                        "type": "message",
                        "role": "assistant",
                        "content": [{"type": "output_text", "text": "  A grounded answer.  "}],
                    }
                ]
            },
            request=httpx.Request(method, url),
        )

    monkeypatch.setattr(llm.httpx, "request", fake_request)
    messages = [
        {"role": "system", "content": "Follow grounding rules."},
        {"role": "user", "content": "How do I improve soil?"},
    ]

    answer = llm._xai(messages, "test-secret", "grok-4.7")

    assert answer == "A grounded answer."
    assert captured["url"] == "https://api.x.ai/v1/responses"
    assert captured["json"] == {"model": "grok-4.7", "input": messages, "store": False}


def test_chat_returns_labeled_knowledge_answer_when_provider_rejects_key(monkeypatch):
    from app.services import rag

    analysis = {
        "cleaned": "How can I improve sandy soil?",
        "keywords": ["improve", "sandy", "soil"],
        "intent": "soil_management",
        "confidence": 0.9,
        "normalized_query": "how can i improve sandy soil",
    }
    source = {
        "document_id": 1,
        "document_title": "Soil preparation",
        "page_number": 1,
        "chunk_id": 1,
        "excerpt": "Add mature compost to improve sandy soil structure.",
        "content": (
            "Sandy loam retains moisture while allowing drainage. "
            "Add mature compost to improve sandy soil structure."
        ),
        "score": 0.8,
        "category": "soil",
    }

    def reject_key(_messages):
        raise rag.LlmError("xAI rejected the configured API key.")

    monkeypatch.setattr(rag, "analyze", lambda _question: analysis)
    monkeypatch.setattr(rag, "retrieve", lambda _db, _question, _analysis: [source])
    monkeypatch.setattr(rag, "get_settings", lambda: SimpleNamespace(llm_configured=True))
    monkeypatch.setattr(rag, "generate", reject_key)

    result = rag.answer_question(None, "How can I improve sandy soil?")

    assert result["llm_status"] == "knowledge_fallback"
    assert "- Add mature compost to improve sandy soil structure." in result["answer"]
    assert "not generated by an AI model" in result["message"]
    assert result["sources"][0]["document_title"] == "Soil preparation"
