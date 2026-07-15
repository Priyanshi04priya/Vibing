from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class RetrievalResult:
    title: str
    kind: str
    score: float
    metadata: dict[str, Any]


class HybridRetriever:
    def __init__(self) -> None:
        self._documents: list[dict[str, Any]] = [
            {
                "title": "Hidden café by the lake",
                "kind": "restaurant",
                "score": 0.93,
                "metadata": {"city": "Delhi", "budget": "low", "food": True, "nature": True},
            },
            {
                "title": "Quiet photography viewpoint",
                "kind": "viewpoint",
                "score": 0.9,
                "metadata": {"city": "Delhi", "photography": True, "nature": True},
            },
            {
                "title": "Student-friendly museum pass",
                "kind": "discount",
                "score": 0.86,
                "metadata": {"city": "Delhi", "budget": "low", "family": False},
            },
        ]

    def retrieve(self, prompt: str, *, limit: int = 3) -> list[RetrievalResult]:
        lowered = prompt.lower()
        filtered = [
            item
            for item in self._documents
            if any(keyword in lowered for keyword in ["food", "view", "photography", "budget", "discount", "quiet", "peaceful"])
        ]
        return [RetrievalResult(**item) for item in filtered[:limit]]
