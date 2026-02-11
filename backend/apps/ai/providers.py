from __future__ import annotations

import hashlib
import math
from typing import Iterable

from django.conf import settings
from openai import OpenAI


def _fallback_embedding(text: str, dim: int = 128) -> list[float]:
    digest = hashlib.sha256(text.encode("utf-8")).digest()
    values = [(digest[i % len(digest)] / 255.0) for i in range(dim)]
    norm = math.sqrt(sum(v * v for v in values)) or 1.0
    return [v / norm for v in values]


class EmbeddingProvider:
    def embed(self, text: str) -> list[float]:
        if settings.OPENAI_API_KEY:
            client = OpenAI(api_key=settings.OPENAI_API_KEY)
            response = client.embeddings.create(model=settings.OPENAI_EMBEDDING_MODEL, input=text)
            return response.data[0].embedding
        return _fallback_embedding(text)


class ChatProvider:
    def answer(self, query: str, contexts: Iterable[str], language: str = "ar") -> str:
        context_text = "\n\n".join(contexts)
        system_prompt = (
            "You are a business intelligence assistant. Respond clearly, accurately, and briefly. "
            "Support Arabic and English. If data is missing, say so."
        )
        user_prompt = f"Question: {query}\n\nContext:\n{context_text}\n\nLanguage: {language}"

        if settings.OPENAI_API_KEY:
            client = OpenAI(api_key=settings.OPENAI_API_KEY)
            response = client.responses.create(
                model=settings.OPENAI_CHAT_MODEL,
                input=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
            )
            return response.output_text
        if language.startswith("ar"):
            return "تم توليد إجابة تجريبية. الرجاء إضافة OPENAI_API_KEY للحصول على إجابات أكثر دقة."
        return "This is a fallback response. Set OPENAI_API_KEY for higher-quality answers."
