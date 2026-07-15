from __future__ import annotations

from app.graphs.langgraph_flow import PlannerGraph
from app.memory.profile import TripMemoryStore
from app.rag.retriever import HybridRetriever
from app.schemas.plan import PlanRequest, TripPlanResponse


class TripGraph(PlannerGraph):
    def __init__(self, memory_store: TripMemoryStore | None = None, retriever: HybridRetriever | None = None) -> None:
        super().__init__(memory_store=memory_store, retriever=retriever)

    def compose(self, request: PlanRequest, user_id: str | None = None) -> TripPlanResponse:
        return self.run(request, user_id=user_id)
