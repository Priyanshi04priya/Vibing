# VibeTrip AI Architecture

## Phase 1 – Architecture and system design

### Goals
- Build a clean, modular GenAI travel planner with LangGraph orchestration.
- Separate concerns into controllers, services, repositories, agents, tools, graphs, prompts, schemas, models, RAG, memory, config, and utils.
- Deliver a polished product experience with an MVP-ready UI.

### Proposed folder structure

```text
apps/
  api/
    app/
      api/
      config/
      controllers/
      models/
      repositories/
      schemas/
      services/
      agents/
      graphs/
      prompts/
      tools/
      rag/
      memory/
      utils/
      main.py
    tests/
  web/
    src/
      app/
      components/
      lib/
      hooks/
      store/
      types/
```

### Core backend modules
- controllers: HTTP endpoints for trip planning and health checks.
- services: orchestration and business logic.
- repositories: persistence abstractions for trips, users, and memory.
- agents: role-based LangGraph agents for mood, budget, weather, planning, food, packing, safety, and story generation.
- tools: distance, weather, budget, maps, restaurant, hotel, fuel, and emergency helpers.
- graphs: LangGraph workflow definition and state management.
- prompts: prompt templates and system instructions.
- schemas: Pydantic request/response models.
- models: ORM/domain models.
- rag: retrieval, chunking, metadata filtering, hybrid search, and citation generation.
- memory: user profile and trip history memory.
- config: environment and dependency configuration.
- utils: logger, errors, ids, and serialization helpers.

### LangGraph flow
1. Intent detection
2. Mood Agent
3. Preference Agent
4. Weather Agent
5. Budget Agent
6. Retrieval Agent
7. Destination Ranking Agent
8. Planner Agent
9. Food Agent
10. Packing Agent
11. Safety Agent
12. Story Agent
13. Final response

### API design
- POST /api/v1/plans/compose
- GET /api/v1/plans/{id}
- GET /api/v1/memory/profile
- GET /api/v1/health

### Data model highlights
- User
- TripPlan
- TripDay
- PlaceRecommendation
- MemoryProfile
- Restaurant
- ExperienceLocation

### Next steps
- Implement the backend module skeleton and API route definitions.
- Add LangGraph graph state and agent stubs.
- Create the frontend planning experience.
- Add RAG indexing and retrieval pipeline.
