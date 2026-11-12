"""Crop guide and the educational recommendation tool."""

import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user
from app.models import CropInformation
from app.schemas import CropCreateRequest, CropOut, RecommendRequest, RecommendResponse
from app.services.recommender import recommend

router = APIRouter(prefix="/api/crops", tags=["crops"])


def _crop_out(row: CropInformation) -> CropOut:
    details = json.loads(row.cultivation_details)
    return CropOut(
        id=row.id,
        crop_name=row.crop_name,
        soil_type=row.soil_type,
        season=row.season,
        description=row.description,
        climate=row.climate,
        water_need=row.water_need,
        suitable_soil=details["suitable_soil"],
        sowing_season=details["sowing_season"],
        organic_fertilizers=details["organic_fertilizers"],
        irrigation=details["irrigation"],
        pest_management=details["pest_management"],
        harvesting=details["harvesting"],
    )


@router.get("", response_model=list[CropOut])
def list_crops(
    q: str | None = None,
    season: str | None = None,
    soil_type: str | None = None,
    db: Session = Depends(get_db),
) -> list[CropOut]:
    query = select(CropInformation)
    if q:
        like = f"%{q.strip()}%"
        query = query.where(or_(CropInformation.crop_name.ilike(like), CropInformation.description.ilike(like)))
    if season:
        query = query.where(CropInformation.season.ilike(f"%{season.strip()}%"))
    if soil_type:
        query = query.where(CropInformation.soil_type.ilike(f"%{soil_type.strip()}%"))
    rows = db.scalars(query.order_by(CropInformation.crop_name)).all()
    return [_crop_out(row) for row in rows]


@router.get("/{crop_id}", response_model=CropOut)
def get_crop(crop_id: int, db: Session = Depends(get_db)) -> CropOut:
    row = db.get(CropInformation, crop_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Crop not found.")
    return _crop_out(row)


@router.post("", response_model=CropOut, status_code=201, dependencies=[Depends(get_current_user)])
def create_crop(
    payload: CropCreateRequest,
    db: Session = Depends(get_db),
) -> CropOut:
    crop_name = payload.crop_name.strip()
    existing = db.scalar(
        select(CropInformation.id).where(CropInformation.crop_name.ilike(crop_name))
    )
    if existing is not None:
        raise HTTPException(status_code=409, detail="A crop with this name already exists.")

    details = {
        "suitable_soil": payload.suitable_soil.strip(),
        "sowing_season": payload.sowing_season.strip(),
        "organic_fertilizers": payload.organic_fertilizers.strip(),
        "irrigation": payload.irrigation.strip(),
        "pest_management": payload.pest_management.strip(),
        "harvesting": payload.harvesting.strip(),
    }
    row = CropInformation(
        crop_name=crop_name,
        soil_type=payload.soil_type.strip(),
        season=payload.season.strip(),
        description=payload.description.strip(),
        cultivation_details=json.dumps(details),
        climate=payload.climate.strip(),
        water_need=payload.water_need.strip(),
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return _crop_out(row)


@router.post("/recommend", response_model=RecommendResponse)
def recommend_crop(payload: RecommendRequest) -> dict:
    return recommend(
        payload.soil_type,
        payload.season,
        payload.water_availability,
        payload.location,
        payload.climate,
    )
