"""Embedding generation.

Production uses sentence-transformers/all-MiniLM-L6-v2.
The deterministic backend exists only for automated tests and is never a
silent fallback when the real model fails.
"""

from __future__ import annotations

import hashlib
import threading

import numpy as np

from app.config import get_settings

_lock = threading.Lock()


def _deterministic_embed(texts: list[str], dim: int = 64) -> np.ndarray:
    vectors = np.zeros((len(texts), dim), dtype=np.float32)
    for row, text in enumerate(texts):
        tokens = [token for token in "".join(ch.lower() if ch.isalnum() else " " for ch in text).split() if len(token) > 2]
        for token in tokens:
            digest = hashlib.md5(token.encode("utf-8")).digest()
            index = int.from_bytes(digest[:4], "little") % dim
            sign = 1.0 if digest[4] % 2 == 0 else -1.0
            vectors[row, index] += sign
        norm = np.linalg.norm(vectors[row])
        if norm == 0:
            vectors[row, 0] = 1.0
        else:
            vectors[row] /= norm
    return vectors


class EmbeddingService:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.backend = self.settings.embedding_backend
        self.model = None
        self.dimension = 64 if self.backend == "deterministic" else 384
        self.error: str | None = None
        self._loading = False

    @property
    def ready(self) -> bool:
        if self.backend == "deterministic":
            return True
        return self.model is not None

    def load(self) -> None:
        if self.backend == "deterministic" or self.model is not None or self._loading:
            return
        with _lock:
            if self.model is not None or self._loading:
                return
            self._loading = True
            try:
                from sentence_transformers import SentenceTransformer

                self.model = SentenceTransformer(self.settings.embedding_model)
                self.dimension = int(self.model.get_sentence_embedding_dimension())
                self.error = None
            except Exception as exc:
                self.error = str(exc)
                self.model = None
            finally:
                self._loading = False

    def embed(self, texts: list[str]) -> np.ndarray:
        if not texts:
            return np.zeros((0, self.dimension), dtype=np.float32)
        if self.backend == "deterministic":
            return _deterministic_embed(texts, self.dimension)
        self.load()
        if self.model is None:
            raise RuntimeError(self.error or "The embedding model is not available.")
        vectors = self.model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=False,
            convert_to_numpy=True,
        )
        return np.asarray(vectors, dtype=np.float32)


_service: EmbeddingService | None = None


def get_embedding_service() -> EmbeddingService:
    global _service
    if _service is None:
        _service = EmbeddingService()
    return _service
