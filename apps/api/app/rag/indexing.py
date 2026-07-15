from __future__ import annotations

from typing import Any

import httpx

from app.config.env import load_config


class QdrantIndexer:
    def __init__(self) -> None:
        self.config = load_config()

    def _build_embedding(self, item: dict[str, Any]) -> list[float]:
        if self.config.gemini_api_key:
            try:
                response = httpx.post(
                    self.config.llm_base_url or "https://generativelanguage.googleapis.com/v1beta/models/embedding-001:embedContent",
                    params={"key": self.config.gemini_api_key},
                    json={
                        "model": "models/embedding-001",
                        "content": {
                            "parts": [{"text": self._to_text(item)}]
                        },
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
        return self._fallback_vector(item)

    def _fallback_vector(self, item: dict[str, Any]) -> list[float]:
        text = self._to_text(item).lower()
        values = [0.0] * 6
        if "food" in text:
            values[0] = 1.0
        if "view" in text or "photography" in text:
            values[1] = 1.0
        if "nature" in text or "water" in text:
            values[2] = 1.0
        if "budget" in text or "cheap" in text:
            values[3] = 1.0
        if "museum" in text or "cafe" in text:
            values[4] = 1.0
        if "peaceful" in text or "calm" in text:
            values[5] = 1.0
        return values

    def _to_text(self, item: dict[str, Any]) -> str:
        return " ".join(
            [
                str(item.get("title", "")),
                str(item.get("kind", "")),
                str(item.get("city", "")),
                str(item.get("description", "")),
                str(item.get("tags", "")),
            ]
        )

    def index_documents(self, documents: list[dict[str, Any]]) -> None:
        if not self.config.enable_qdrant or not self.config.qdrant_url:
            return

        try:
            from qdrant_client import QdrantClient
            from qdrant_client.http import models as rest
        except Exception:
            return

        client = QdrantClient(url=self.config.qdrant_url, api_key=self.config.qdrant_api_key)
        try:
            client.get_collection(self.config.qdrant_collection)
        except Exception:
            client.create_collection(
                collection_name=self.config.qdrant_collection,
                vectors_config=rest.VectorParams(size=768, distance=rest.Distance.COSINE),
                optimizers_config=rest.OptimizersConfigDiff(memmap_threshold=20000),
            )

        points = []
        for idx, item in enumerate(documents):
            payload = {
                "title": item.get("title", "travel spot"),
                "kind": item.get("kind", "location"),
                "city": item.get("city", "Delhi"),
                "state": item.get("state", "Delhi"),
                "budget": item.get("budget", "low"),
                "season": item.get("season", "all"),
                "transport": item.get("transport", "cab"),
                "family": item.get("family", False),
                "friends": item.get("friends", True),
                "couples": item.get("couples", False),
                "solo": item.get("solo", False),
                "kids": item.get("kids", False),
                "photography": item.get("photography", False),
                "adventure": item.get("adventure", False),
                "nature": item.get("nature", True),
                "food": item.get("food", False),
                "rating": item.get("rating", 4.5),
                "distance": item.get("distance", 40),
                "description": item.get("description", "A curated travel experience."),
                "tags": item.get("tags", []),
            }
            points.append(
                rest.PointStruct(
                    id=idx + 1,
                    vector=self._build_embedding(item),
                    payload=payload,
                )
            )

        client.upsert(collection_name=self.config.qdrant_collection, points=points)
