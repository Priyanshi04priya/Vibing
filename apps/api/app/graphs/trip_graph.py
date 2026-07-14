from app.agents.budget_agent import estimate_budget
from app.agents.mood_agent import extract_mood
from app.agents.planner_agent import build_itinerary
from app.schemas.plan import PlanRequest, TripPlanResponse


class TripGraph:
    def compose(self, request: PlanRequest) -> TripPlanResponse:
        mood_profile = extract_mood(request)
        budget_profile = estimate_budget(request)
        itinerary = build_itinerary(request, mood_profile, budget_profile)

        destination = "Sohna Road & Damdama Lake" if "delhi" in request.prompt.lower() else "Mcleodganj"
        return TripPlanResponse(
            title=f"{mood_profile['mood'].title()} escape for {request.preferences.companions if request.preferences else 2} travelers",
            summary=(
                f"A {mood_profile['energy_level']} paced plan shaped around {mood_profile['mood']} energy, "
                f"with a budget of ₹{budget_profile['total_budget']} and thoughtful food stops."
            ),
            destination=destination,
            total_budget=budget_profile["total_budget"],
            transportation="Private cab + local transit",
            estimated_duration="One day getaway",
            itinerary=itinerary,
            food_recommendations=[
                "Hidden kulfi stall near the lake",
                "Vegetarian thali café with sunset views",
                "Street food tasting trail",
            ],
            hidden_gems=[
                "Photography point by the water",
                "Quiet viewpoint after the main trail",
                "Local market for handmade gifts",
            ],
            packing_list=["Water bottle", "Power bank", "Light jacket", "Sunglasses", "Snacks"],
            safety_notes=["Carry a printed address", "Avoid isolated turns after dusk", "Keep cash for local vendors"],
            instagram_caption="A slow, cinematic escape designed around good food, quiet views, and the right amount of adventure.",
        )
