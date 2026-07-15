import os
from dataclasses import dataclass


@dataclass
class AppConfig:
    gemini_api_key: str | None = None
    gemini_model: str = "gemini-2.0-flash"
    llm_base_url: str | None = None
    qdrant_url: str | None = None
    qdrant_api_key: str | None = None
    qdrant_collection: str = "vibetrip"
    enable_qdrant: bool = False


def load_config() -> AppConfig:
    return AppConfig(
        gemini_api_key=os.getenv("GEMINI_API_KEY"),
        gemini_model=os.getenv("GEMINI_MODEL", "gemini-2.0-flash"),
        llm_base_url=os.getenv("LLM_BASE_URL", "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"),
        qdrant_url=os.getenv("QDRANT_URL"),
        qdrant_api_key=os.getenv("QDRANT_API_KEY"),
        qdrant_collection=os.getenv("QDRANT_COLLECTION", "vibetrip"),
        enable_qdrant=os.getenv("ENABLE_QDRANT", "false").lower() == "true",
    )
