from __future__ import annotations

from typing import Any, TypedDict


class PlanningState(TypedDict, total=False):
    request: Any
    prompt: str
    user_id: str | None
    mood_profile: dict[str, Any]
    preferences: dict[str, Any]
    budget_profile: dict[str, Any]
    weather: dict[str, Any]
    retrieval_results: list[Any]
    itinerary: list[Any]
    food_recommendations: list[str]
    hidden_gems: list[str]
    packing_list: list[str]
    safety_notes: list[str]
    story: str
    memory_summary: str
    destination: str
    title: str
    summary: str
    total_budget: int
    transportation: str
    estimated_duration: str
    instagram_caption: str
