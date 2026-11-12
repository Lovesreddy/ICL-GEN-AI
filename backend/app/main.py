"""Application entry point."""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import select, text

from app.config import get_settings
from app.database import SessionLocal, engine
from app.models import Base
from app.routers import admin, auth, chat, crops, knowledge, nlp, photo_guide, tools
from app.services.seed import index_samples, seed_admin, seed_crops

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("organic_farming")


def init_database() -> None:
    Base.metadata.create_all(bind=engine)
    with engine.begin() as connection:
        connection.execute(
            text(
                "CREATE TABLE IF NOT EXISTS schema_migrations "
                "(version VARCHAR(64) PRIMARY KEY, applied_at TIMESTAMP NOT NULL)"
            )
        )
        existing = connection.execute(
            text("SELECT version FROM schema_migrations WHERE version = '001_initial'")
        ).first()
        if existing is None:
            connection.execute(
                text("INSERT INTO schema_migrations (version, applied_at) VALUES ('001_initial', CURRENT_TIMESTAMP)")
            )


def startup_tasks() -> None:
    settings = get_settings()
    db = SessionLocal()
    try:
        seed_admin(db)
        seed_crops(db)
        if settings.auto_index:
            logger.info("Indexing sample knowledge documents.")
            index_samples(db)
            logger.info("Sample indexing finished.")
    except Exception:
        logger.exception("Startup indexing failed.")
    finally:
        db.close()


@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_database()
    settings = get_settings()
    if settings.jwt_secret == "change-me-in-the-environment":
        logger.warning("JWT_SECRET is still the default. Set a private value in backend/.env.")
    startup_tasks()
    yield


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_name, version="1.0.0", lifespan=lifespan)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(auth.router)
    app.include_router(chat.router)
    app.include_router(knowledge.router)
    app.include_router(crops.router)
    app.include_router(tools.router)
    app.include_router(photo_guide.router)
    app.include_router(nlp.router)
    app.include_router(admin.router)

    @app.exception_handler(Exception)
    async def unhandled(_request: Request, exc: Exception):
        logger.exception("Unhandled error")
        return JSONResponse(status_code=500, content={"detail": "The server could not complete this request."})

    @app.get("/")
    def root() -> dict:
        return {"name": settings.app_name, "docs": "/docs", "health": "/api/health"}

    return app


init_database()
app = create_app()
