"""Curated knowledge, fertilizer, and pest articles."""

from fastapi import APIRouter, HTTPException, Query

from app.data.library import DISCLAIMER, FERTILIZERS, KNOWLEDGE, PESTS

router = APIRouter(prefix="/api", tags=["knowledge"])

COLLECTIONS = {
    "knowledge": KNOWLEDGE,
    "fertilizers": FERTILIZERS,
    "pests": PESTS,
}


def _filter(items: list[dict], q: str | None, category: str | None) -> list[dict]:
    results = []
    needle = (q or "").strip().lower()
    for item in items:
        if category and item["category"] != category:
            continue
        blob = " ".join(
            [item["title"], item["summary"], item["description"], " ".join(item["related_crops"])]
        ).lower()
        if needle and needle not in blob:
            continue
        results.append({**item, "disclaimer": DISCLAIMER})
    return results


@router.get("/knowledge")
def knowledge(q: str | None = None, category: str | None = None) -> list[dict]:
    return _filter(KNOWLEDGE, q, category)


@router.get("/knowledge/{article_id}")
def knowledge_detail(article_id: str) -> dict:
    for item in KNOWLEDGE:
        if item["id"] == article_id:
            return {**item, "disclaimer": DISCLAIMER}
    raise HTTPException(status_code=404, detail="Knowledge article not found.")


@router.get("/fertilizers")
def fertilizers(q: str | None = Query(default=None)) -> list[dict]:
    return _filter(FERTILIZERS, q, None)


@router.get("/fertilizers/{article_id}")
def fertilizer_detail(article_id: str) -> dict:
    for item in FERTILIZERS:
        if item["id"] == article_id:
            return {**item, "disclaimer": DISCLAIMER}
    raise HTTPException(status_code=404, detail="Fertilizer guide not found.")


@router.get("/pests")
def pests(q: str | None = None) -> list[dict]:
    return _filter(PESTS, q, None)


@router.get("/pests/{article_id}")
def pest_detail(article_id: str) -> dict:
    for item in PESTS:
        if item["id"] == article_id:
            return {**item, "disclaimer": DISCLAIMER}
    raise HTTPException(status_code=404, detail="Pest guide not found.")
