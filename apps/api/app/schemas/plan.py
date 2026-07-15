from pydantic import BaseModel, Field


class TripPreferences(BaseModel):
    mood: str = Field(default="calm")
    energy_level: str = Field(default="medium")
    adventure: str = Field(default="balanced")
    travel_style: str = Field(default="slow")
    social_preference: str = Field(default="friends")
    budget: int = Field(default=2500)
    duration_hours: int | None = Field(default=8)
    start_city: str = Field(default="Delhi")
    companions: int = Field(default=4)


class PlanRequest(BaseModel):
    prompt: str = Field(..., min_length=10)
    preferences: TripPreferences | None = None


class ItineraryStep(BaseModel):
    time: str
    title: str
    description: str
    budget_estimate: int


class TripPlanResponse(BaseModel):
    title: str
    summary: str
    destination: str
    total_budget: int
    transportation: str
    estimated_duration: str
    itinerary: list[ItineraryStep]
    food_recommendations: list[str]
    hidden_gems: list[str]
    packing_list: list[str]
    safety_notes: list[str]
    instagram_caption: str
    memory_summary: str | None = None
