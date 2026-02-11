import re


def split_sentences_arabic_aware(text: str) -> list[str]:
    normalized = text.replace("\r\n", "\n").strip()
    if not normalized:
        return []
    pieces = re.split(r"(?<=[\.\!\?\u061F\u06D4])\s+|\n{2,}", normalized)
    return [piece.strip() for piece in pieces if piece.strip()]


def chunk_text(text: str, chunk_size: int = 800, overlap: int = 120) -> list[str]:
    sentences = split_sentences_arabic_aware(text)
    if not sentences:
        return []

    chunks: list[str] = []
    current = ""
    for sentence in sentences:
        candidate = f"{current} {sentence}".strip()
        if len(candidate) <= chunk_size:
            current = candidate
            continue
        if current:
            chunks.append(current)
        overlap_text = current[-overlap:] if current else ""
        current = f"{overlap_text} {sentence}".strip()
    if current:
        chunks.append(current)
    return chunks
