"""Groq, xAI/Grok, and Gemini chat calls with explicit configuration errors."""

from __future__ import annotations

import base64
import time

import httpx

from app.config import get_settings


class LlmNotConfigured(RuntimeError):
    pass


class LlmError(RuntimeError):
    pass


def llm_status() -> dict:
    settings = get_settings()
    provider = settings.llm_provider.lower().strip()
    configured = settings.llm_configured
    if provider in {"gemini", "google"}:
        model = settings.gemini_model
        key_name = "GEMINI_API_KEY"
    elif provider in {"grok", "xai"}:
        model = settings.xai_model
        key_name = "GROK_API_KEY"
    else:
        model = settings.groq_model
        key_name = "GROQ_API_KEY"
    if configured:
        message = f"{provider} is configured with model {model}."
    else:
        message = f"{key_name} is not set. The assistant will show retrieved sources and will not invent an answer."
    return {"provider": provider, "model": model, "configured": configured, "message": message}


def generate(messages: list[dict[str, str]]) -> str:
    settings = get_settings()
    provider = settings.llm_provider.lower().strip()
    if provider in {"gemini", "google"}:
        if not settings.gemini_api_key:
            raise LlmNotConfigured("GEMINI_API_KEY is not set.")
        return _gemini(messages, settings.gemini_api_key, settings.gemini_model)
    if provider in {"grok", "xai"}:
        if not settings.xai_api_key:
            raise LlmNotConfigured("GROK_API_KEY is not set.")
        return _xai(messages, settings.xai_api_key, settings.xai_model)
    if not settings.groq_api_key:
        raise LlmNotConfigured("GROQ_API_KEY is not set.")
    return _groq(messages, settings.groq_api_key, settings.groq_model)


def analyze_image(image: bytes, content_type: str, prompt: str) -> str:
    settings = get_settings()
    if not settings.groq_api_key:
        raise LlmNotConfigured("GROQ_API_KEY is not set for photo analysis.")
    return _groq_vision(image, content_type, prompt, settings.groq_api_key, settings.groq_vision_model)


def _request_with_retries(
    method: str,
    url: str,
    *,
    auth_error: str,
    timeout_seconds: float = 40.0,
    **kwargs,
) -> httpx.Response:
    last_error = "The language model did not respond."
    for attempt in range(3):
        try:
            response = httpx.request(method, url, timeout=timeout_seconds, **kwargs)
        except httpx.TimeoutException as exc:
            last_error = "The language model timed out."
            if attempt == 2:
                raise LlmError(last_error) from exc
            time.sleep(1.5 * (attempt + 1))
            continue
        except httpx.HTTPError as exc:
            raise LlmError("The language model could not be reached.") from exc
        if response.status_code == 429 or response.status_code >= 500:
            last_error = f"The language model returned HTTP {response.status_code}."
            if attempt == 2:
                raise LlmError(last_error)
            time.sleep(1.5 * (attempt + 1))
            continue
        if response.status_code in {401, 403}:
            raise LlmError(auth_error)
        if response.status_code >= 400:
            detail = response.text[:300]
            raise LlmError(f"The language model request failed ({response.status_code}): {detail}")
        return response
    raise LlmError(last_error)


def _groq(messages: list[dict[str, str]], api_key: str, model: str) -> str:
    response = _request_with_retries(
        "POST",
        "https://api.groq.com/openai/v1/chat/completions",
        auth_error=(
            "Groq rejected the configured API key. Replace GROQ_API_KEY in backend/.env "
            "with a valid key, then restart the backend."
        ),
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={"model": model, "temperature": 0.2, "max_tokens": 900, "messages": messages},
    )
    payload = response.json()
    try:
        return payload["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError, AttributeError) as exc:
        raise LlmError("Groq returned a response without answer text.") from exc


def _groq_vision(image: bytes, content_type: str, prompt: str, api_key: str, model: str) -> str:
    encoded_image = base64.b64encode(image).decode("ascii")
    response = _request_with_retries(
        "POST",
        "https://api.groq.com/openai/v1/chat/completions",
        auth_error=(
            "Groq rejected the configured API key. Replace GROQ_API_KEY in backend/.env "
            "with a valid key, then restart the backend."
        ),
        timeout_seconds=60.0,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={
            "model": model,
            "temperature": 0.2,
            "max_completion_tokens": 900,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are a cautious agricultural photo guide. Describe only what is visible, separate "
                        "observations from possibilities, and use the user's crop and notes as context. Do not "
                        "claim a definitive disease, pest, nutrient deficiency, soil pH, or fertilizer identity "
                        "from a photo alone. Never prescribe pesticide or fertilizer rates. Give practical, low-risk "
                        "next steps and say when a soil test, product label, or local agricultural expert is needed. "
                        "If the image is unclear or unrelated to farming, say so plainly."
                    ),
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:{content_type};base64,{encoded_image}"},
                        },
                    ],
                },
            ],
        },
    )
    payload = response.json()
    try:
        content = payload["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise LlmError("Groq returned an image-analysis response without answer text.") from exc
    if isinstance(content, str) and content.strip():
        return content.strip()
    if isinstance(content, list):
        text = "\n".join(
            part["text"].strip()
            for part in content
            if isinstance(part, dict) and part.get("type") == "text"
            and isinstance(part.get("text"), str) and part["text"].strip()
        )
        if text:
            return text
    raise LlmError("Groq returned an image-analysis response without answer text.")


def _xai(messages: list[dict[str, str]], api_key: str, model: str) -> str:
    response = _request_with_retries(
        "POST",
        "https://api.x.ai/v1/responses",
        auth_error=(
            "xAI rejected the configured API key. Replace GROK_API_KEY (or XAI_API_KEY) "
            "in backend/.env with a valid key, then restart the backend."
        ),
        timeout_seconds=120.0,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={"model": model, "input": messages, "store": False},
    )
    payload = response.json()
    answer = payload.get("output_text")
    if isinstance(answer, str) and answer.strip():
        return answer.strip()

    output = payload.get("output")
    if isinstance(output, list):
        text_parts = [
            part["text"].strip()
            for item in output
            if isinstance(item, dict) and item.get("type") == "message" and item.get("role") == "assistant"
            for part in item.get("content", [])
            if isinstance(part, dict) and part.get("type") == "output_text" and isinstance(part.get("text"), str)
            and part["text"].strip()
        ]
        if text_parts:
            return "\n".join(text_parts)
    raise LlmError("Grok Responses API returned a response without answer text.")


def _gemini(messages: list[dict[str, str]], api_key: str, model: str) -> str:
    system = "\n".join(item["content"] for item in messages if item["role"] == "system")
    user = "\n\n".join(item["content"] for item in messages if item["role"] == "user")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    response = _request_with_retries(
        "POST",
        url,
        auth_error=(
            "Google rejected the configured API key. Replace GEMINI_API_KEY in backend/.env "
            "with a valid key, then restart the backend."
        ),
        params={"key": api_key},
        headers={"Content-Type": "application/json"},
        json={
            "systemInstruction": {"parts": [{"text": system}]},
            "contents": [{"role": "user", "parts": [{"text": user}]}],
            "generationConfig": {"temperature": 0.2, "maxOutputTokens": 900},
        },
    )
    payload = response.json()
    try:
        return payload["candidates"][0]["content"]["parts"][0]["text"].strip()
    except (KeyError, IndexError, AttributeError) as exc:
        raise LlmError("Gemini returned a response without answer text.") from exc
