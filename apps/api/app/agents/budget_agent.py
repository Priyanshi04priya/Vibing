def estimate_budget(request) -> dict[str, int]:
    base_budget = request.preferences.budget if request.preferences else 2500
    transport = max(600, int(base_budget * 0.25))
    food = max(500, int(base_budget * 0.2))
    tickets = max(300, int(base_budget * 0.15))
    buffer = max(250, int(base_budget * 0.1))
    total_budget = transport + food + tickets + buffer
    return {
        "transport": transport,
        "food": food,
        "tickets": tickets,
        "buffer": buffer,
        "total_budget": min(total_budget, base_budget + 500),
    }
