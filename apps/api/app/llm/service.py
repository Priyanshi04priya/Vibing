import os

import httpx

from app.config.env import load_config


class LLMService:
    def __init__(self, api_key: str | None = None, base_url: str | None = None, model: str | None = None) -> None:
        config = load_config()
        self.api_key = api_key or config.gemini_api_key or os.getenv("GOOGLE_API_KEY")
        self.base_url = base_url or config.llm_base_url or "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
        self.model = model or config.gemini_model or "gemini-2.0-flash"

    def generate(self, prompt: str, *, temperature: float = 0.2) -> str:
        if self.api_key:
            try:
                response = httpx.post(
                    self.base_url,
                    params={"key": self.api_key},
                    json={
                        "contents": [{"parts": [{"text": prompt}]}],
                        "generationConfig": {"temperature": temperature},
                    },
                    timeout=15.0,
                )
                response.raise_for_status()
                payload = response.json()
                candidates = payload.get("candidates") or []
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    if parts:
                        return parts[0].get("text", "")
            except Exception:
                pass

        return self._fallback(prompt)

    def _fallback(self, prompt: str) -> str:
        lower_prompt = prompt.lower()
        if "mood" in lower_prompt or "energy" in lower_prompt:
            return "restorative"
        if "story" in lower_prompt:
            return "A calm, cinematic escape with good food and a soft sunset finish."
        if "food" in lower_prompt:
            return "street-food trail, vegetarian cafe, and a hidden dessert stop"
        return "balanced"
