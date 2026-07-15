from app.graphs.trip_graph import TripGraph
from app.memory.profile import TripMemoryStore
from app.schemas.plan import PlanRequest, TripPreferences


def test_graph_uses_memory_for_food_suggestions() -> None:
    memory_store = TripMemoryStore()
    memory_store.remember_trip(
        "user-1",
        {
            "destination": "Sohna",
            "favorite_cuisine": "biryani",
            "budget": 2500,
            "transport": "cab",
        },
    )

    graph = TripGraph(memory_store=memory_store)
    request = PlanRequest(
        prompt="I need peaceful places with good food for a one-day trip from Delhi.",
        preferences=TripPreferences(budget=2500, start_city="Delhi", companions=4),
    )

    plan = graph.compose(request, user_id="user-1")

    assert plan.destination
    assert plan.food_recommendations
    assert any("biryani" in item.lower() for item in plan.food_recommendations)
    assert plan.memory_summary
