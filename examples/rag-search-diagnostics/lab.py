"""Minimal offline FAISS retrieval diagnostics lab.

Uses two synthetic 2-D vectors to show one real failure mode: asking FAISS for
more neighbours than exist returns the -1 sentinel, and a naive Python filter
turns that sentinel into the last item of the metadata list.

This proves label handling only. It does not embed text, measure semantic
retrieval quality, or call a model. No network, model, or API key is needed.
"""

from __future__ import annotations

import json

import faiss
import numpy as np

CHUNKS = [
    {"path": "cancel_order.py"},
    {"path": "archive_order.py"},
]
VECTORS = np.array([[0.0, 0.0], [1.0, 0.0]], dtype=np.float32)
QUERY = np.array([[0.1, 0.0]], dtype=np.float32)
K = 5


def build_index(kind: str) -> faiss.Index:
    """Build a real FAISS index with only two vectors."""
    if kind == "flat":
        index = faiss.IndexFlatL2(VECTORS.shape[1])
    elif kind == "hnsw":
        index = faiss.IndexHNSWFlat(VECTORS.shape[1], 32)
    else:
        raise ValueError(f"unsupported index: {kind}")
    index.add(VECTORS)
    return index


def search(index: faiss.Index, query: np.ndarray = QUERY, k: int = K):
    """Return raw FAISS distances and labels, including any -1 padding."""
    distances, labels = index.search(query, k)
    return distances[0].tolist(), labels[0].tolist()


def paths_original_filter(labels, chunks=CHUNKS):
    """The 2024 filter `if i < len(chunks)`; Python accepts -1."""
    return [chunks[i]["path"] for i in labels if i < len(chunks)]


def paths_bounded_filter(labels, chunks=CHUNKS):
    """Corrected filter: keep only labels that address real metadata."""
    return [chunks[i]["path"] for i in labels if 0 <= i < len(chunks)]


def case(kind: str) -> dict:
    index = build_index(kind)
    distances, labels = search(index)
    return {
        "index": kind,
        "ntotal": index.ntotal,
        "k": K,
        "labels": labels,
        "distances": [
            None if not np.isfinite(d) else round(float(d), 4) for d in distances
        ],
        "original_filter": paths_original_filter(labels),
        "bounded_filter": paths_bounded_filter(labels),
    }


def empty_index_case() -> dict:
    """Deliberately inconsistent fixture: zero vectors, retained chunk metadata.

    This is not a normal path of the original code. `create_index` returns
    (None, None) when no embedding succeeds, and with empty metadata the
    original filter would raise IndexError instead of inventing a chunk. The
    fixture exists to test loading an index and its metadata separately.
    """
    index = faiss.IndexFlatL2(VECTORS.shape[1])
    distances, labels = search(index)
    return {
        "ntotal": index.ntotal,
        "labels": labels,
        "distances": [
            None if not np.isfinite(d) else round(float(d), 4) for d in distances
        ],
        "original_filter": paths_original_filter(labels),
        "bounded_filter": paths_bounded_filter(labels),
    }


def invalid_metadata_case() -> dict:
    """A stale label beyond the metadata list must not be treated as a chunk."""
    labels = [0, 7, -1]
    return {
        "labels": labels,
        "original_filter": paths_original_filter(labels),
        "bounded_filter": paths_bounded_filter(labels),
    }


def metric_demo() -> dict:
    """Squared L2 and cosine on unit vectors: distance is not confidence."""
    a = np.array([1.0, 0.0], dtype=np.float32)
    b = np.array([0.6, 0.8], dtype=np.float32)
    cosine = float(np.dot(a, b))
    l2_squared = float(np.sum((a - b) ** 2))
    return {
        "cosine": round(cosine, 4),
        "l2_squared": round(l2_squared, 4),
        "identity_2_minus_2cos": round(2 - 2 * cosine, 4),
        "score_1_over_1_plus_l2_squared": round(1 / (1 + l2_squared), 4),
    }


def main() -> None:
    result = {
        "purpose": "Synthetic vectors; proves label handling, not embedding or LLM quality",
        "chunks": [chunk["path"] for chunk in CHUNKS],
        "query": QUERY[0].tolist(),
        "cases": [case("flat"), case("hnsw")],
        "empty_index": empty_index_case(),
        "invalid_metadata": invalid_metadata_case(),
        "metric": metric_demo(),
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
