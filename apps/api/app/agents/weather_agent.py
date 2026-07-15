from __future__ import annotations

from typing import Any


def build_weather_advice(request: Any) -> dict[str, Any]:
    prompt = request.prompt.lower()
    if "rain" in prompt or "cloud" in prompt:
        return {"forecast": "Rain likely", "advice": "Swap the long walk for indoor cafés and a museum stop."}
    if "tired" in prompt or "exam" in prompt:
        return {"forecast": "Pleasant", "advice": "Keep the day short and restorative with a sunset finish."}
    return {"forecast": "Clear", "advice": "Plan for open-air viewpoints and a longer photo walk."}
