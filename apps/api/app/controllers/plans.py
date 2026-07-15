from fastapi import APIRouter

from app.schemas.plan import PlanRequest, TripPlanResponse
from app.services.planner_service import planner_service

router = APIRouter(prefix="/api/v1/plans", tags=["plans"])


@router.post("/compose", response_model=TripPlanResponse)
async def compose_plan(request: PlanRequest) -> TripPlanResponse:
    return planner_service.compose_plan(request)


@router.post("/compose-with-memory/{user_id}", response_model=TripPlanResponse)
async def compose_plan_with_memory(user_id: str, request: PlanRequest) -> TripPlanResponse:
    return planner_service.compose_plan(request, user_id=user_id)


@router.get("/{plan_id}")
async def get_plan(plan_id: str) -> dict[str, str]:
    return {"plan_id": plan_id, "status": "ready"}
