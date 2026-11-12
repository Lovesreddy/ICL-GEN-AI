"""Document ingestion: extract, clean, chunk, embed, and index."""

from __future__ import annotations

import importlib.util
import shutil
from pathlib import Path

import numpy as np
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import get_settings
from app.models import ChatSource, Document, DocumentChunk
from app.services.chunking import chunk_pages
from app.services.embeddings import get_embedding_service
from app.services.extraction import ExtractionError, extract_document
from app.services.nlp_service import clean_text
from app.services.vector_store import get_vector_store

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt"}
ALLOWED_CATEGORIES = {
    "soil",
    "fertilizer",
    "compost",
    "pest",
    "crop",
    "water",
    "certification",
    "general",
}


def validate_upload(filename: str, size: int, category: str) -> str:
    settings = get_settings()
    suffix = Path(filename).suffix.lower()
    if suffix not in ALLOWED_EXTENSIONS:
        raise ExtractionError("Upload a PDF, DOCX, or TXT file.")
    if suffix == ".pdf" and importlib.util.find_spec("fitz") is None:
        raise ExtractionError("PDF uploads are unavailable on this deployment.")
    if suffix == ".docx" and importlib.util.find_spec("docx") is None:
        raise ExtractionError("DOCX uploads are unavailable on this deployment.")
    if size > settings.max_upload_mb * 1024 * 1024:
        raise ExtractionError(f"Files must be {settings.max_upload_mb} MB or smaller.")
    if size <= 0:
        raise ExtractionError("The uploaded file is empty.")
    if category not in ALLOWED_CATEGORIES:
        raise ExtractionError("Choose a valid document category.")
    header_ok = True
    return suffix if header_ok else suffix


def check_signature(path: Path) -> None:
    data = path.read_bytes()[:8]
    suffix = path.suffix.lower()
    if suffix == ".pdf" and not data.startswith(b"%PDF"):
        raise ExtractionError("The file does not look like a valid PDF.")
    if suffix == ".docx" and not data.startswith(b"PK"):
        raise ExtractionError("The file does not look like a valid DOCX document.")
    if suffix == ".txt":
        data.decode("utf-8")


def safe_filename(name: str) -> str:
    cleaned = "".join(char if char.isalnum() or char in "._-" else "_" for char in Path(name).name)
    return cleaned[:120] or "document.txt"


def ingest_file(
    db: Session,
    path: Path,
    title: str,
    category: str,
    source_type: str,
    original_name: str | None = None,
) -> Document:
    document = db.scalar(select(Document).where(Document.stored_path == str(path)))
    if document is None:
        document = Document(
            filename=original_name or path.name,
            title=title,
            category=category,
            stored_path=str(path),
            source_type=source_type,
            processing_status="processing",
        )
        db.add(document)
    else:
        document.processing_status = "processing"
        document.error_message = None
        document.title = title
        document.category = category
    db.commit()
    db.refresh(document)
    try:
        _reindex_document(db, document)
    except Exception as exc:
        document.processing_status = "failed"
        document.error_message = str(exc)[:500]
        document.chunk_count = 0
        db.commit()
        raise
    return document


def reindex_document(db: Session, document: Document) -> Document:
    document.processing_status = "processing"
    document.error_message = None
    db.commit()
    try:
        _reindex_document(db, document)
    except Exception as exc:
        document.processing_status = "failed"
        document.error_message = str(exc)[:500]
        db.commit()
        raise
    return document


def _reindex_document(db: Session, document: Document) -> None:
    path = Path(document.stored_path)
    if not path.exists():
        raise ExtractionError("The stored file is missing.")
    pages = extract_document(path)
    chunks = chunk_pages(pages)
    if not chunks:
        raise ExtractionError("The document did not produce any usable text chunks.")
    embedder = get_embedding_service()
    vectors = embedder.embed([chunk["content"] for chunk in chunks])
    old_ids = [row.id for row in document.chunks]
    if old_ids:
        db.query(ChatSource).filter(ChatSource.chunk_id.in_(old_ids)).update(
            {ChatSource.chunk_id: None}, synchronize_session=False
        )
        get_vector_store().delete(old_ids)
        for chunk in list(document.chunks):
            db.delete(chunk)
        db.flush()
    stored: list[DocumentChunk] = []
    for index, chunk in enumerate(chunks):
        row = DocumentChunk(
            document_id=document.id,
            chunk_index=index,
            content=chunk["content"],
            page_number=chunk["page_number"],
            token_count=chunk["token_count"],
            category=document.category,
            embedding=np.asarray(vectors[index], dtype=np.float32).tobytes(),
        )
        db.add(row)
        stored.append(row)
    db.flush()
    get_vector_store().add([row.id for row in stored], vectors)
    document.chunk_count = len(stored)
    document.processing_status = "ready"
    document.error_message = None
    db.commit()
    db.refresh(document)


def delete_document(db: Session, document: Document) -> None:
    ids = [chunk.id for chunk in document.chunks]
    source_type = document.source_type
    path = Path(document.stored_path)
    if ids:
        get_vector_store().delete(ids)
    db.delete(document)
    db.commit()
    if source_type == "upload" and path.exists():
        path.unlink()


def save_upload(filename: str, payload: bytes) -> Path:
    settings = get_settings()
    directory = settings.resolve(settings.knowledge_dir) / "uploads"
    directory.mkdir(parents=True, exist_ok=True)
    from uuid import uuid4

    path = directory / f"{uuid4().hex[:10]}-{safe_filename(filename)}"
    path.write_bytes(payload)
    try:
        check_signature(path)
    except UnicodeDecodeError as exc:
        path.unlink(missing_ok=True)
        raise ExtractionError("Text files must be UTF-8.") from exc
    except ExtractionError:
        path.unlink(missing_ok=True)
        raise
    return path


def remove_path(path: Path) -> None:
    if path.exists():
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()
