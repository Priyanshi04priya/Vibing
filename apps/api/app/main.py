from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.controllers.plans import router as plans_router

app = FastAPI(title="VibeTrip AI API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(plans_router)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
