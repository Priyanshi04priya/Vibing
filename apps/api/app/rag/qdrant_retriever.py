from __future__ import annotations

import httpx

from app.config.env import load_config
from app.rag.retriever import RetrievalResult


class QdrantRetriever:
    def __init__(self) -> None:
        self.config = load_config()
        self._enabled = self.config.enable_qdrant and bool(self.config.qdrant_url)

    def is_enabled(self) -> bool:
        return self._enabled

    def retrieve(self, prompt: str, *, limit: int = 3) -> list[RetrievalResult]:
        if not self.is_enabled():
            return []

        try:
            from qdrant_client import QdrantClient
            from qdrant_client.http import models as rest
        except Exception:
            return []

        client = QdrantClient(url=self.config.qdrant_url, api_key=self.config.qdrant_api_key)
        filters = rest.Filter(
            must=[
                rest.FieldCondition(key="city", match=rest.MatchValue(value="Delhi")),
                rest.FieldCondition(key="food", match=rest.MatchValue(value=True)),
            ]
        )
        hits = client.search(
            collection_name=self.config.qdrant_collection,
            query_vector=self._build_query_vector(prompt),
            limit=limit,
            query_filter=filters,
        )
        return [
            RetrievalResult(
                title=str(item.payload.get("title", "Qdrant result")),
                kind=str(item.payload.get("kind", "location")),
                score=float(getattr(item, "score", 0.0) or 0.0),
                metadata=dict(item.payload),
            )
            for item in hits
        ]

    def _build_query_vector(self, prompt: str) -> list[float]:
        if self.config.gemini_api_key:
            try:
                response = httpx.post(
                    "https://generativelanguage.googleapis.com/v1beta/models/embedding-001:embedContent",
                    params={"key": self.config.gemini_api_key},
                    json={
                        "model": "models/embedding-001",
                        "content": {"parts": [{"text": prompt}]},
                    },
                    timeout=15.0,
                )
                response.raise_for_status()
                payload = response.json()
                embedding = payload.get("embedding", {}).get("values")
                if embedding:
                    return [float(v) for v in embedding]
            except Exception:
                pass
        return self._fallback_vector(prompt)

    def _fallback_vector(self, prompt: str) -> list[float]:
        lowered = prompt.lower()
        values = [0.0] * 768
        if "food" in lowered:
            values[0] = 1.0
        if "view" in lowered or "photography" in lowered:
            values[1] = 1.0
        if "nature" in lowered or "water" in lowered:
            values[2] = 1.0
        if "budget" in lowered or "cheap" in lowered:
            values[3] = 1.0
        if "museum" in lowered or "cafe" in lowered:
            values[4] = 1.0
        if "peaceful" in lowered or "calm" in lowered:
            values[5] = 1.0
        return values
