"""Create sample documents, crop rows, and the optional administrator account."""

import json
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import get_settings
from app.data.crops import CROPS
from app.data.library import FERTILIZERS, KNOWLEDGE, PESTS, render_article, render_crop
from app.models import CropInformation, Document, User
from app.security import hash_password
from app.services.ingestion import ingest_file


def seed_admin(db: Session) -> None:
    settings = get_settings()
    if not settings.admin_email or not settings.admin_password:
        return
    email = settings.admin_email.lower()
    existing = db.scalar(select(User).where(User.email == email))
    if existing:
        return
    legacy_admin = db.scalar(select(User).where(User.email == "admin@organicfarm.local"))
    if legacy_admin:
        legacy_admin.email = email
        db.commit()
        return
    db.add(
        User(
            name=settings.admin_name,
            email=email,
            password_hash=hash_password(settings.admin_password),
            role="administrator",
        )
    )
    db.commit()


def seed_crops(db: Session) -> None:
    existing_names = {
        name.lower()
        for name in db.scalars(select(CropInformation.crop_name)).all()
    }
    for crop in CROPS:
        if crop["crop_name"].lower() in existing_names:
            continue
        details = {
            "suitable_soil": crop["suitable_soil"],
            "sowing_season": crop["sowing_season"],
            "organic_fertilizers": crop["organic_fertilizers"],
            "irrigation": crop["irrigation"],
            "pest_management": crop["pest_management"],
            "harvesting": crop["harvesting"],
        }
        db.add(
            CropInformation(
                crop_name=crop["crop_name"],
                soil_type=crop["soil_type"],
                season=crop["season"],
                description=crop["description"],
                cultivation_details=json.dumps(details),
                climate=crop["climate"],
                water_need=crop["water_need"],
            )
        )
        existing_names.add(crop["crop_name"].lower())
    db.commit()


def write_sample_files() -> list[tuple[Path, str, str]]:
    settings = get_settings()
    root = settings.resolve(settings.knowledge_dir) / "samples"
    root.mkdir(parents=True, exist_ok=True)
    written: list[tuple[Path, str, str]] = []
    articles = [(item, "knowledge") for item in KNOWLEDGE]
    articles += [(item, "fertilizer") for item in FERTILIZERS]
    articles += [(item, "pest") for item in PESTS]
    for article, _kind in articles:
        path = root / f"{article['id']}.txt"
        if not path.exists():
            path.write_text(render_article(article), encoding="utf-8")
        written.append((path, article["title"], article["category"]))
    for crop in CROPS:
        slug = crop["crop_name"].lower().replace(" ", "-")
        path = root / f"crop-{slug}.txt"
        if not path.exists():
            path.write_text(render_crop(crop), encoding="utf-8")
        written.append((path, f"{crop['crop_name']} cultivation", "crop"))
    return written


def index_samples(db: Session) -> None:
    for path, title, category in write_sample_files():
        existing = db.scalar(select(Document).where(Document.stored_path == str(path)))
        if existing and existing.processing_status == "ready" and existing.chunk_count > 0:
            continue
        ingest_file(db, path, title, category, "sample", path.name)
