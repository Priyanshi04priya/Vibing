from app.graphs.trip_graph import TripGraph
from app.memory.profile import TripMemoryStore
from app.repositories.database import create_user, init_db, save_trip
from app.schemas.plan import PlanRequest, TripPlanResponse


class PlannerService:
    def __init__(self) -> None:
        self.memory_store = TripMemoryStore()
        self.graph = TripGraph(memory_store=self.memory_store)

    def compose_plan(self, request: PlanRequest, *, user_id: str | None = None) -> TripPlanResponse:
        init_db()
        if user_id:
            create_user(user_id)
            self.memory_store.remember_trip(
                user_id,
                {
                    "destination": "Delhi escape",
                    "favorite_cuisine": "biryani",
                    "budget": request.preferences.budget if request.preferences else 2500,
                    "transport": "cab",
                },
            )
        plan = self.graph.compose(request, user_id=user_id)
        if user_id:
            save_trip(user_id, destination=plan.destination, summary=plan.summary, budget=plan.total_budget)
        return plan


planner_service = PlannerService()
