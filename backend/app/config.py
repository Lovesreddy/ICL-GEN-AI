"""Runtime configuration loaded from environment variables."""

from functools import lru_cache
from pathlib import Path

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_ROOT = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    app_name: str = "Organic Farming Guide"
    database_url: str = "sqlite:///./data/organic_farming.db"
    jwt_secret: str = "change-me-in-the-environment"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60 * 24
    admin_email: str | None = None
    admin_password: str | None = None
    admin_name: str = "Administrator"
    llm_provider: str = "groq"
    groq_api_key: str | None = None
    groq_model: str = "openai/gpt-oss-20b"
    groq_vision_model: str = "qwen/qwen3.8-27b"
    gemini_api_key: str | None = None
    gemini_model: str = "gemini-2.0-flash"
    xai_api_key: str | None = Field(
        default=None,
        validation_alias=AliasChoices("xai_api_key", "grok_api_key"),
    )
    xai_model: str = Field(default="grok-4.7", validation_alias=AliasChoices("xai_model", "grok_model"))
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    embedding_backend: str = "sentence-transformers"
    vector_dir: str = "./data/vector_store"
    knowledge_dir: str = "./knowledge_base"
    auto_index: bool = True
    relevance_threshold: float = 0.28
    retrieval_k: int = 4
    max_upload_mb: int = 10
    cors_origins: str = (
        "http://localhost:5173,http://127.0.0.1:5173,"
        "http://localhost:5174,http://127.0.0.1:5174,"
        "http://localhost:5175,http://127.0.0.1:5175"
    )

    model_config = SettingsConfigDict(
        env_file=str(BACKEND_ROOT / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    def resolve(self, value: str) -> Path:
        path = Path(value)
        if not path.is_absolute():
            path = BACKEND_ROOT / path
        return path

    @property
    def cors_origin_list(self) -> list[str]:
        return [item.strip() for item in self.cors_origins.split(",") if item.strip()]

    @property
    def llm_configured(self) -> bool:
        provider = self.llm_provider.lower().strip()
        if provider in {"gemini", "google"}:
            return bool(self.gemini_api_key)
        if provider in {"grok", "xai"}:
            return bool(self.xai_api_key)
        return bool(self.groq_api_key)


@lru_cache
def get_settings() -> Settings:
    return Settings()
