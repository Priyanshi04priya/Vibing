import os
from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.base import Base
from app.models.trip import Trip
from app.models.user import User

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/vibetrip")
engine = create_engine(DATABASE_URL, future=True)


def init_db() -> None:
    try:
        Base.metadata.create_all(engine)
    except SQLAlchemyError:
        pass


def create_user(user_id: str, *, name: str | None = None, email: str | None = None) -> User:
    try:
        with Session(engine) as session:
            user = session.get(User, user_id)
            if user is None:
                user = User(id=user_id, name=name, email=email)
                session.add(user)
                session.commit()
                session.refresh(user)
            return user
    except SQLAlchemyError:
        return User(id=user_id, name=name, email=email)


def save_trip(user_id: str, *, destination: str, summary: str, budget: int) -> Trip:
    try:
        with Session(engine) as session:
            trip = Trip(id=f"{user_id}-{len(session.query(Trip).filter(Trip.user_id == user_id).all()) + 1}", user_id=user_id, destination=destination, summary=summary, budget=budget)
            session.add(trip)
            session.commit()
            session.refresh(trip)
            return trip
    except SQLAlchemyError:
        return Trip(id=f"{user_id}-1", user_id=user_id, destination=destination, summary=summary, budget=budget)


def list_trips(user_id: str) -> list[dict[str, Any]]:
    try:
        with Session(engine) as session:
            trips = session.query(Trip).filter(Trip.user_id == user_id).all()
            return [{"id": trip.id, "destination": trip.destination, "summary": trip.summary, "budget": trip.budget} for trip in trips]
    except SQLAlchemyError:
        return []
