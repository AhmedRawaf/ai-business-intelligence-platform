import math
from typing import Iterable

from apps.documents.models import DocumentChunk


def cosine_similarity(a: list[float], b: list[float]) -> float:
    if not a or not b:
        return 0.0
    length = min(len(a), len(b))
    a = a[:length]
    b = b[:length]
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a)) or 1.0
    norm_b = math.sqrt(sum(y * y for y in b)) or 1.0
    return dot / (norm_a * norm_b)


def retrieve_top_chunks(organization_id: int, query_embedding: list[float], top_k: int = 5) -> list[DocumentChunk]:
    chunks = DocumentChunk.objects.filter(organization_id=organization_id).select_related("document")
    scored = [(chunk, cosine_similarity(query_embedding, chunk.embedding or [])) for chunk in chunks]
    scored.sort(key=lambda item: item[1], reverse=True)
    return [item[0] for item in scored[:top_k]]


def build_citations(chunks: Iterable[DocumentChunk]) -> list[dict]:
    citations = []
    for chunk in chunks:
        citations.append(
            {
                "document_name": chunk.document.name,
                "snippet": chunk.snippet,
                "page": chunk.metadata.get("page"),
                "chunk_index": chunk.chunk_index,
            }
        )
    return citations
