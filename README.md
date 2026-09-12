# UniNexus AI

**Autonomous Multi-Agent University Intelligence Platform**

Built by **ZARAK KHAN**

A modular AI platform with real multi-agent orchestration, local LLM planning (no paid APIs), multi-tenant data isolation, JWT auth, and automated tests.

---

## What This Is

Not a chatbot. A genuine multi-agent system:

- **Orchestrator** plans tasks and delegates to specialized agents
- **Local LLM** (Ollama llama3.2) for intelligent planning - free, offline
- **4 real agents** - Attendance, Policy, Risk, Knowledge - query a live database
- **Multi-tenant** - strict isolation between universities
- **Full audit trail** - every agent execution is persisted
- **12 automated tests** - all passing

---

## Tech Stack

| Layer | Choice |
|-------|--------|
| Backend | FastAPI, SQLAlchemy, SQLite/PostgreSQL |
| Frontend | React 19, Vite, Tailwind CSS v4 |
| Charts | Recharts |
| Auth | JWT, bcrypt |
| LLM | Ollama llama3.2 - local, free |
| Tests | pytest, httpx |

---

## Quick Start

### Backend

    cd F:\UniNexus-AI
    python -m venv .venv
    .\.venv\Scripts\Activate.ps1
    python -m pip install fastapi uvicorn sqlalchemy pydantic-settings python-jose passlib python-multipart email-validator ollama pytest httpx
    python seed_demo_data.py
    python seed_documents.py
    uvicorn backend.app.main:app --reload

Backend runs at http://127.0.0.1:8000, docs at /docs

### Frontend

    cd frontend
    npm install
    npm run dev

Frontend runs at http://localhost:5173

### Local LLM (optional)

    ollama pull llama3.2:1b

If Ollama is not running, the platform falls back to keyword-based planning.

### Default Login

- Email: admin@demo.university.edu
- Password: securepassword123
- Tenant ID: 1

---

## Testing

    .\.venv\Scripts\Activate.ps1
    python -m pytest tests/ -v

Expected: 12 passed

---

## Project Structure

    UniNexus-AI/
      backend/app/
        agents/       BaseAgent, Orchestrator, specialized agents, registry
        api/          auth, agents, stats, academic, analytics
        core/         config, database, security, LLM wrapper
        models/       SQLAlchemy models
        schemas/      Pydantic schemas
        main.py       FastAPI entry
      frontend/src/
        api/          Axios client with JWT interceptor
        components/   Layout, AgentResult
        pages/        Login, Register, Dashboard, CommandCenter, Analytics
      tests/          pytest suite
      seed_demo_data.py
      seed_documents.py
      .env.example
      README.md

---

## Honest Limitations

This is a portfolio demonstration, not production software:

- No real university integration - uses a Demo University
- Small LLM llama3.2 - free and local but less capable than GPT-4
- Keyword search only - semantic RAG is on the roadmap
- No human approval UI yet - architecture supports it
- SQLite in dev - production would use PostgreSQL

---

## Roadmap

- Semantic RAG with vector embeddings
- Human approval workflow
- Email and in-app notifications
- LMS connectors (Moodle, Canvas via LTI)
- Docker Compose for one-command deploy

---

## License

MIT

**Built by ZARAK KHAN** - UniNexus AI, 2026
