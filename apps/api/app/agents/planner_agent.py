from app.schemas.plan import ItineraryStep


def build_itinerary(request, mood_profile, budget_profile) -> list[ItineraryStep]:
    return [
        ItineraryStep(
            time="08:30",
            title="Slow breakfast and café stop",
            description="Start with a quiet breakfast and coffee before heading to the main destination.",
            budget_estimate=450,
        ),
        ItineraryStep(
            time="10:30",
            title="Scenic walk and photo spots",
            description="Choose a calm route with viewpoints, local markets, and shade-heavy stops.",
            budget_estimate=300,
        ),
        ItineraryStep(
            time="14:00",
            title="Lunch and local food crawl",
            description="Prioritize hidden eateries and one signature local dish.",
            budget_estimate=600,
        ),
        ItineraryStep(
            time="17:00",
            title="Sunset and return",
            description="Wrap with a relaxed sunset stop and a buffer for traffic or delays.",
            budget_estimate=250,
        ),
    ]
