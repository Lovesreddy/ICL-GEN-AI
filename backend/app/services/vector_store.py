"""Persistent FAISS index. Chunk text and metadata live in SQLite."""

from __future__ import annotations

import json
import threading
from pathlib import Path

import faiss
import numpy as np

from app.config import get_settings


class VectorStore:
    def __init__(self) -> None:
        settings = get_settings()
        self.directory = settings.resolve(settings.vector_dir)
        self.directory.mkdir(parents=True, exist_ok=True)
        self.index_path = self.directory / "index.faiss"
        self.meta_path = self.directory / "meta.json"
        self.lock = threading.Lock()
        self.index: faiss.Index | None = None
        self.dimension: int | None = None
        self._load()

    def _load(self) -> None:
        if self.index_path.exists() and self.meta_path.exists():
            meta = json.loads(self.meta_path.read_text(encoding="utf-8"))
            self.dimension = int(meta["dimension"])
            self.index = faiss.read_index(str(self.index_path))

    def save(self) -> None:
        if self.index is None:
            return
        faiss.write_index(self.index, str(self.index_path))
        self.meta_path.write_text(
            json.dumps({"dimension": self.dimension, "count": self.count()}),
            encoding="utf-8",
        )

    def count(self) -> int:
        return 0 if self.index is None else int(self.index.ntotal)

    def reset(self, dimension: int) -> None:
        with self.lock:
            self.dimension = dimension
            self.index = faiss.IndexIDMap2(faiss.IndexFlatIP(dimension))
            self.save()

    def _ensure(self, dimension: int) -> None:
        if self.index is None:
            self.dimension = dimension
            self.index = faiss.IndexIDMap2(faiss.IndexFlatIP(dimension))
        elif self.dimension != dimension:
            raise RuntimeError(
                f"Embedding dimension changed from {self.dimension} to {dimension}. "
                "Reindex the knowledge base with one embedding model."
            )

    def add(self, ids: list[int], vectors: np.ndarray) -> None:
        if len(ids) == 0:
            return
        matrix = np.ascontiguousarray(vectors, dtype=np.float32)
        faiss.normalize_L2(matrix)
        with self.lock:
            self._ensure(matrix.shape[1])
            self.index.add_with_ids(matrix, np.asarray(ids, dtype=np.int64))
            self.save()

    def delete(self, ids: list[int]) -> None:
        if not ids or self.index is None:
            return
        with self.lock:
            self.index.remove_ids(np.asarray(ids, dtype=np.int64))
            self.save()

    def search(self, vector: np.ndarray, k: int) -> list[tuple[int, float]]:
        if self.index is None or self.count() == 0:
            return []
        query = np.ascontiguousarray(vector.reshape(1, -1), dtype=np.float32)
        faiss.normalize_L2(query)
        with self.lock:
            scores, ids = self.index.search(query, min(k, self.count()))
        results = []
        for score, chunk_id in zip(scores[0], ids[0]):
            if int(chunk_id) == -1:
                continue
            results.append((int(chunk_id), float(score)))
        return results

    def status(self) -> dict:
        return {
            "status": "ready" if self.index is not None else "empty",
            "vectors": self.count(),
            "dimension": self.dimension,
            "path": str(self.directory),
        }


_store: VectorStore | None = None


def get_vector_store() -> VectorStore:
    global _store
    if _store is None:
        _store = VectorStore()
    return _store


def clear_vector_store_files(directory: Path) -> None:
    for name in ("index.faiss", "meta.json"):
        file = directory / name
        if file.exists():
            file.unlink()
