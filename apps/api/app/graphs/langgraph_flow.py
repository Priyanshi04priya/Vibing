from __future__ import annotations

from typing import Any

from langgraph.graph import END, StateGraph

from app.agents.budget_agent import estimate_budget
from app.agents.food_agent import pick_food_recommendations
from app.agents.mood_agent import extract_mood
from app.agents.packing_agent import build_packing_list
from app.agents.planner_agent import build_itinerary
from app.agents.preference_agent import extract_preferences
from app.agents.safety_agent import build_safety_notes
from app.agents.weather_agent import build_weather_advice
from app.graphs.state import PlanningState
from app.llm.service import LLMService
from app.memory.profile import TripMemoryStore
from app.rag.qdrant_retriever import QdrantRetriever
from app.rag.retriever import HybridRetriever, RetrievalResult
from app.schemas.plan import ItineraryStep, PlanRequest, TripPlanResponse


class PlannerGraph:
    def __init__(self, memory_store: TripMemoryStore | None = None, retriever: HybridRetriever | None = None) -> None:
        self.memory_store = memory_store or TripMemoryStore()
        self.fallback_retriever = retriever or HybridRetriever()
        self.qdrant_retriever = QdrantRetriever()
        self.retriever = self.qdrant_retriever if self.qdrant_retriever.is_enabled() else self.fallback_retriever
        self.llm = LLMService()
        self.workflow = self._build_workflow()

    def _build_workflow(self) -> StateGraph:
        workflow = StateGraph(PlanningState)
        workflow.add_node("mood", self._mood_node)
        workflow.add_node("preferences", self._preference_node)
        workflow.add_node("budget", self._budget_node)
        workflow.add_node("weather", self._weather_node)
        workflow.add_node("retrieval", self._retrieval_node)
        workflow.add_node("planner", self._planner_node)
        workflow.add_node("food", self._food_node)
        workflow.add_node("packing", self._packing_node)
        workflow.add_node("safety", self._safety_node)
        workflow.add_node("story", self._story_node)
        workflow.add_edge("mood", "preferences")
        workflow.add_edge("preferences", "budget")
        workflow.add_edge("budget", "weather")
        workflow.add_edge("weather", "retrieval")
        workflow.add_edge("retrieval", "planner")
        workflow.add_edge("planner", "food")
        workflow.add_edge("food", "packing")
        workflow.add_edge("packing", "safety")
        workflow.add_edge("safety", "story")
        workflow.add_edge("story", END)
        workflow.set_entry_point("mood")
        return workflow.compile()

    def _mood_node(self, state: PlanningState) -> dict[str, Any]:
        request = state["request"]
        return {"mood_profile": extract_mood(request)}

    def _preference_node(self, state: PlanningState) -> dict[str, Any]:
        request = state["request"]
        memory_profile = self.memory_store.get_profile(state.get("user_id") or "default")
        return {"preferences": extract_preferences(request, memory_profile)}

    def _budget_node(self, state: PlanningState) -> dict[str, Any]:
        request = state["request"]
        return {"budget_profile": estimate_budget(request)}

    def _weather_node(self, state: PlanningState) -> dict[str, Any]:
        request = state["request"]
        return {"weather": build_weather_advice(request)}

    def _retrieval_node(self, state: PlanningState) -> dict[str, Any]:
        request = state["request"]
        return {"retrieval_results": self.retriever.retrieve(request.prompt)}

    def _planner_node(self, state: PlanningState) -> dict[str, Any]:
        request = state["request"]
        itinerary = build_itinerary(request, state["mood_profile"], state["budget_profile"])
        return {"itinerary": itinerary}

    def _food_node(self, state: PlanningState) -> dict[str, Any]:
        return {"food_recommendations": pick_food_recommendations(state["preferences"], state.get("retrieval_results", []))}

    def _packing_node(self, state: PlanningState) -> dict[str, Any]:
        return {"packing_list": build_packing_list()}

    def _safety_node(self, state: PlanningState) -> dict[str, Any]:
        return {"safety_notes": build_safety_notes()}

    def _story_node(self, state: PlanningState) -> dict[str, Any]:
        request = state["request"]
        story = self.llm.generate(f"Create a short travel story for: {request.prompt}")
        memory_profile = self.memory_store.get_profile(state.get("user_id") or "default")
        return {
            "story": story,
            "memory_summary": f"Memory: {', '.join(memory_profile.get('favorite_destinations', [])[:3]) or 'new traveler'}",
        }

    def run(self, request: PlanRequest, user_id: str | None = None) -> TripPlanResponse:
        state = {
            "request": request,
            "user_id": user_id,
            "prompt": request.prompt,
        }
        result = self.workflow.invoke(state)
        mood_profile = result["mood_profile"]
        budget_profile = result["budget_profile"]
        destination = "Sohna Road & Damdama Lake" if "delhi" in request.prompt.lower() else "Mcleodganj"
        return TripPlanResponse(
            title=f"{mood_profile['mood'].title()} escape for {request.preferences.companions if request.preferences else 2} travelers",
            summary=(
                f"A {mood_profile['energy_level']} paced plan shaped around {mood_profile['mood']} energy. "
                f"{result['weather']['advice']}"
            ),
            destination=destination,
            total_budget=budget_profile["total_budget"],
            transportation="Private cab + local transit",
            estimated_duration="One day getaway",
            itinerary=[
                ItineraryStep(
                    time=step.time,
                    title=step.title,
                    description=step.description,
                    budget_estimate=step.budget_estimate,
                )
                for step in result["itinerary"]
            ],
            food_recommendations=result["food_recommendations"],
            hidden_gems=[item.title for item in result.get("retrieval_results", [])[:2]],
            packing_list=result["packing_list"],
            safety_notes=result["safety_notes"],
            instagram_caption=result["story"],
            memory_summary=result.get("memory_summary"),
        )
