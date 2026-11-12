"""Fertilizer calculator and FAQ search."""

from fastapi import APIRouter, HTTPException, Query

from app.data.library import FAQS
from app.schemas import FaqOut, FertilizerRequest, FertilizerResponse
from app.services.fertilizer import calculate

router = APIRouter(prefix="/api", tags=["tools"])


@router.post("/fertilizer/calculate", response_model=FertilizerResponse)
def fertilizer_calculate(payload: FertilizerRequest) -> dict:
    try:
        return calculate(payload.crop, payload.land_area, payload.area_unit, payload.fertilizer_type)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.get("/faq", response_model=list[FaqOut])
def faq(q: str | None = None, category: str | None = Query(default=None)) -> list[dict]:
    needle = (q or "").strip().lower()
    results = []
    for item in FAQS:
        if category and item["category"].lower() != category.lower():
            continue
        if needle and needle not in item["question"].lower() and needle not in item["answer"].lower():
            continue
        results.append(item)
    return results
