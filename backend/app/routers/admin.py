"""Health, public statistics, and administrator dashboard."""

from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import require_admin
from app.models import ChatMessage, Document, DocumentChunk, User
from app.schemas import DashboardOut, DocumentOut
from app.services.embeddings import get_embedding_service
from app.services.extraction import ExtractionError
from app.services.ingestion import delete_document, ingest_file, reindex_document, save_upload, validate_upload
from app.services.llm import llm_status
from app.services.nlp_service import _lemmatizer_name, ensure_nlp_ready
from app.services.vector_store import get_vector_store

router = APIRouter(prefix="/api", tags=["admin"])


def build_health(db: Session) -> dict:
    database = "ok"
    try:
        db.execute(select(func.count()).select_from(User))
    except Exception as exc:
        database = f"error: {exc}"
    embedder = get_embedding_service()
    ensure_nlp_ready()
    return {
        "status": "ok" if database == "ok" else "degraded",
        "database": database,
        "vector_store": get_vector_store().status(),
        "llm": llm_status(),
        "nlp": {"status": "ok", "lemmatizer": _lemmatizer_name},
        "embeddings": {
            "backend": embedder.backend,
            "model": embedder.settings.embedding_model,
            "ready": embedder.ready,
            "error": embedder.error,
        },
    }


@router.get("/health")
def health(db: Session = Depends(get_db)) -> dict:
    return build_health(db)


@router.get("/stats")
def stats(db: Session = Depends(get_db)) -> dict:
    return {
        "documents": db.scalar(select(func.count()).select_from(Document)) or 0,
        "chunks": db.scalar(select(func.count()).select_from(DocumentChunk)) or 0,
        "crops": 10,
        "topics": 10,
    }


@router.get("/admin/dashboard", response_model=DashboardOut)
def dashboard(db: Session = Depends(get_db), _admin=Depends(require_admin)) -> dict:
    category_rows = db.execute(
        select(Document.category, func.count()).group_by(Document.category).order_by(Document.category)
    ).all()
    recent = db.scalars(select(Document).order_by(Document.upload_date.desc()).limit(6)).all()
    return {
        "users": db.scalar(select(func.count()).select_from(User)) or 0,
        "documents": db.scalar(select(func.count()).select_from(Document)) or 0,
        "chunks": db.scalar(select(func.count()).select_from(DocumentChunk)) or 0,
        "queries": db.scalar(select(func.count()).select_from(ChatMessage).where(ChatMessage.role == "user")) or 0,
        "recent_documents": recent,
        "documents_by_category": [{"category": name, "count": count} for name, count in category_rows],
        "health": build_health(db),
    }


@router.get("/admin/documents", response_model=list[DocumentOut])
def list_documents(db: Session = Depends(get_db), _admin=Depends(require_admin)) -> list[Document]:
    return list(db.scalars(select(Document).order_by(Document.upload_date.desc())).all())


@router.post("/admin/documents/upload", response_model=DocumentOut)
async def upload_document(
    file: UploadFile = File(...),
    category: str = Form(...),
    title: str = Form(""),
    db: Session = Depends(get_db),
    _admin=Depends(require_admin),
) -> Document:
    payload = await file.read()
    try:
        validate_upload(file.filename or "document.txt", len(payload), category)
        path = save_upload(file.filename or "document.txt", payload)
        document = ingest_file(
            db,
            path,
            title.strip() or (file.filename or path.name),
            category,
            "upload",
            file.filename or path.name,
        )
    except ExtractionError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    if document.processing_status == "failed":
        raise HTTPException(status_code=422, detail=document.error_message or "Document processing failed.")
    return document


@router.delete("/admin/documents/{document_id}", status_code=204)
def remove_document(document_id: int, db: Session = Depends(get_db), _admin=Depends(require_admin)) -> None:
    document = db.get(Document, document_id)
    if document is None:
        raise HTTPException(status_code=404, detail="Document not found.")
    delete_document(db, document)


@router.post("/admin/documents/{document_id}/reindex", response_model=DocumentOut)
def reindex(document_id: int, db: Session = Depends(get_db), _admin=Depends(require_admin)) -> Document:
    document = db.get(Document, document_id)
    if document is None:
        raise HTTPException(status_code=404, detail="Document not found.")
    try:
        return reindex_document(db, document)
    except Exception as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
