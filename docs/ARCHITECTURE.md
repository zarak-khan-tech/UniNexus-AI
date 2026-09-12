# Architecture

## Overview

UniNexus AI is a two-tier application:

- **FastAPI backend** — REST API, agent orchestration, database access
- **React frontend** — professional UI for issuing tasks and viewing results

## Multi-Agent Flow

1. User submits a natural-language task via the Command Center
2. Orchestrator plans the task using the **local LLM** (Ollama)
   - If Ollama is unavailable, falls back to a deterministic keyword router
3. The plan is validated — agents must exist in the registry
4. Each agent runs in sequence; results are collected
5. The full execution (plan + results + duration) is persisted to `agent_executions`
6. The response is returned to the frontend as structured JSON

## Agents

Every agent inherits from `BaseAgent` and implements `execute(task) -> dict`.

| Agent | Responsibility |
|-------|----------------|
| AttendanceAgent | Fetches students with low attendance |
| PolicyAgent | Returns institutional policy thresholds |
| RiskAgent | Analyzes risk from attendance + grades |
| KnowledgeAgent | Keyword-searches policy documents |

New agents can be added by creating a class and registering it — the orchestrator code doesn't change.

## Multi-Tenancy

Every sensitive model carries a `tenant_id` foreign key:

- User, Student, Course, Document, AgentExecution

All API endpoints filter by `current_user.tenant_id`. No query ever returns cross-tenant data.

## Authentication

- JWT tokens (HS256) with 30-minute expiry
- Passwords hashed with bcrypt
- Protected endpoints use a `get_current_active_user` dependency
- Frontend stores the token in `localStorage` and injects it via an Axios interceptor

## Database

- **Development:** SQLite (`uninexus.db`, lives on F: drive)
- **Production path:** PostgreSQL (same SQLAlchemy models)

Tables created automatically at application startup via `Base.metadata.create_all()`.

## Testing

12 pytest tests use an in-memory SQLite instance. The FastAPI `get_db` dependency is overridden to point at the test session — no side effects on real data.

Run with:

## LLM Integration

`backend/app/core/llm.py` wraps Ollama:

- `check_ollama_status()` — reports available models
- `plan_with_llm(user_request, agents)` — returns a validated JSON plan or `None`

Uses `format='json'` and `keep_alive='30m'` for reliability and speed. Falls back gracefully when Ollama is not running.
