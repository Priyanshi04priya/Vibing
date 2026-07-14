from app.graphs.trip_graph import TripGraph
from app.schemas.plan import PlanRequest, TripPlanResponse


class PlannerService:
    def __init__(self) -> None:
        self.graph = TripGraph()

    def compose_plan(self, request: PlanRequest) -> TripPlanResponse:
        return self.graph.compose(request)


planner_service = PlannerService()
