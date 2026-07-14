def extract_mood(request) -> dict[str, str]:
    prompt = request.prompt.lower()
    mood = "peaceful"
    if "tired" in prompt or "exam" in prompt:
        mood = "restorative"
    if "adventure" in prompt or "thrill" in prompt:
        mood = "adventurous"
    energy_level = "low"
    if "budget" in prompt and "2500" in prompt:
        energy_level = "medium"
    return {"mood": mood, "energy_level": energy_level}
