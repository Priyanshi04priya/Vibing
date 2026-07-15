from __future__ import annotations

from typing import Any


def extract_preferences(request: Any, memory_profile: dict[str, Any] | None = None) -> dict[str, Any]:
    memory_profile = memory_profile or {}
    prompt = request.prompt.lower()
    return {
        "travel_style": "slow" if "peaceful" in prompt or "calm" in prompt else "balanced",
        "social_preference": "friends" if "friends" in prompt else "solo",
        "food_preference": memory_profile.get("favorite_cuisines", ["local cafes"])[0] if memory_profile.get("favorite_cuisines") else "local cafes",
        "budget_mode": "budget" if (request.preferences and request.preferences.budget and request.preferences.budget <= 3000) else "balanced",
    }
