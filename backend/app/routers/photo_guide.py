"""Image-assisted crop and field observations."""

from collections import defaultdict, deque
from threading import Lock
from time import monotonic
from typing import Literal

from fastapi import APIRouter, File, Form, HTTPException, Request, UploadFile

from app.config import get_settings
from app.schemas import PhotoGuideAnalysisResponse
from app.services.llm import LlmError, LlmNotConfigured, analyze_image

router = APIRouter(prefix="/api/photo-guide", tags=["photo guide"])
MAX_IMAGE_BYTES = 10 * 1024 * 1024
RATE_WINDOW_SECONDS = 60 * 60
MAX_ANALYSES_PER_WINDOW = 8
_analysis_requests: dict[str, deque[float]] = defaultdict(deque)
_analysis_lock = Lock()
VALID_IMAGE_SIGNATURES = {
    "image/jpeg": (b"\xff\xd8\xff",),
    "image/png": (b"\x89PNG\r\n\x1a\n",),
}


@router.post("/analyze", response_model=PhotoGuideAnalysisResponse)
async def analyze_photo(
    request: Request,
    image: UploadFile = File(...),
    crop_name: str = Form(..., max_length=80),
    subject_type: Literal["crop", "soil", "fertilizer"] = Form(...),
    notes: str = Form("", max_length=1000),
    consent_to_provider: bool = Form(False),
) -> PhotoGuideAnalysisResponse:
    if not consent_to_provider:
        raise HTTPException(
            status_code=400,
            detail="Confirm that you want to send this photo and its notes to Groq for analysis.",
        )

    content_type = image.content_type or ""
    signatures = VALID_IMAGE_SIGNATURES.get(content_type)
    if signatures is None:
        raise HTTPException(status_code=415, detail="Choose a JPEG or PNG image.")

    try:
        image_bytes = await image.read(MAX_IMAGE_BYTES + 1)
    finally:
        await image.close()
    if len(image_bytes) > MAX_IMAGE_BYTES:
        raise HTTPException(status_code=413, detail="Images must be 10 MB or smaller.")
    if not any(image_bytes.startswith(signature) for signature in signatures):
        raise HTTPException(status_code=415, detail="The uploaded file is not a valid JPEG or PNG image.")

    settings = get_settings()
    if not settings.groq_api_key:
        raise HTTPException(status_code=503, detail="Photo analysis is not configured. Set GROQ_API_KEY in backend/.env.")
    client_ip = request.client.host if request.client else "unknown"
    now = monotonic()
    with _analysis_lock:
        requests = _analysis_requests[client_ip]
        while requests and now - requests[0] >= RATE_WINDOW_SECONDS:
            requests.popleft()
        if len(requests) >= MAX_ANALYSES_PER_WINDOW:
            raise HTTPException(
                status_code=429,
                detail="Photo analysis is limited to 8 requests per hour from this network. Please try again later.",
            )
        requests.append(now)

    prompt = (
        f"Photo subject: {subject_type}\n"
        f"Crop or context: {crop_name}\n"
        f"User observations and question: {notes.strip() or 'No additional notes provided.'}\n\n"
        "Respond with a concise, easy-to-understand assessment of this image and the user's question. "
        "Explain visible clues, uncertainty, and safe next steps."
    )
    try:
        answer = analyze_image(image_bytes, content_type, prompt)
    except LlmNotConfigured as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except LlmError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    return PhotoGuideAnalysisResponse(answer=answer, model=settings.groq_vision_model)
