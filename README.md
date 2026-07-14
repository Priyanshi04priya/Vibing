# VibeTrip AI

VibeTrip AI is a production-grade GenAI travel planner that transforms a mood-based prompt into a complete weekend experience. The project is structured as a monorepo with a FastAPI backend and a Next.js frontend, designed for phased development and future deployment.

## Current status
- Monorepo scaffold created
- FastAPI health endpoint implemented
- Next.js landing experience implemented
- Architecture and roadmap documented

## Planned phases
1. Architecture and system design
2. Backend services and LangGraph graph skeleton
3. Frontend planner experience
4. RAG pipeline and embeddings
5. Deployment and observability
6. Testing and documentation

## Run locally

### Backend
```bash
cd apps/api
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
cd apps/web
npm install
npm run dev
```
