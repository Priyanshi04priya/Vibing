from __future__ import annotations

from collections import defaultdict
from typing import Any


class TripMemoryStore:
    def __init__(self) -> None:
        self._store: dict[str, list[dict[str, Any]]] = defaultdict(list)

    def remember_trip(self, user_id: str, trip: dict[str, Any]) -> None:
        self._store[user_id].append(trip)

    def get_profile(self, user_id: str) -> dict[str, Any]:
        trips = self._store.get(user_id, [])
        if not trips:
            return {"favorite_destinations": [], "favorite_cuisines": [], "preferred_transport": None}

        favorite_cuisines = [trip.get("favorite_cuisine") for trip in trips if trip.get("favorite_cuisine")]
        favorite_destinations = [trip.get("destination") for trip in trips if trip.get("destination")]
        preferred_transport = next((trip.get("transport") for trip in reversed(trips) if trip.get("transport")), None)
        return {
            "favorite_destinations": favorite_destinations,
            "favorite_cuisines": favorite_cuisines,
            "preferred_transport": preferred_transport,
        }
