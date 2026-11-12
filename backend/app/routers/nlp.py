"""NLP inspection endpoint."""

from fastapi import APIRouter

from app.schemas import NlpRequest, NlpResponse
from app.services.nlp_service import analyze

router = APIRouter(prefix="/api/nlp", tags=["nlp"])


@router.post("/analyze", response_model=NlpResponse)
def analyze_text(payload: NlpRequest) -> dict:
    return analyze(payload.text, payload.compare_to)
