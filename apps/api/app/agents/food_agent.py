from __future__ import annotations

from typing import Any


def pick_food_recommendations(preferences: dict[str, Any], retrieval_results: list[Any] | None = None) -> list[str]:
    base = [
        f"{preferences.get('food_preference', 'local cafes')} tasting stop",
        "Vegetarian cafe with a calm patio",
        "Street-food trail for a shared bite",
    ]
    if retrieval_results:
        base.append(retrieval_results[0].title)
    return base
