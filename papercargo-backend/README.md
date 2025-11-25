# Papercargo Backend (MVP)

## Local dev (Docker Compose)
1. Copy `.env.example` to `.env` and set values.
2. docker compose up --build

This brings up:
- Postgres on 5432
- Redis on 6379
- FastAPI app on 8000
- Celery worker in separate container

## Endpoints
- GET /api/health
- POST /api/setup-db
- POST /api/agents/create
- POST /api/agents/{agent_id}/run  (body: event JSON)

## Notes
- Agent runtime is currently a simple skeleton in `app/agents/agent_core.py`.
- Replace the SimpleAgent with your real planner / RAG / model calls.
