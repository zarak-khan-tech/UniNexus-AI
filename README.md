# UniNexus AI

**Autonomous Multi-Agent University Intelligence Platform**

Built by **ZARAK KHAN**

UniNexus AI is a portfolio-focused university intelligence platform built around a real multi-agent architecture. It is designed as an intelligent layer over university systems such as LMS, SIS, ERP, and institutional portals.

> **This is not a chatbot.** An orchestrator plans tasks and delegates them to specialized agents that work with university data and institutional knowledge.

---

## What Makes It Different

- **Agent Orchestration** — a central Orchestrator plans and delegates tasks
- **4 Specialized Agents** — Attendance, Policy, Risk, and Knowledge
- **Local LLM Planning** — Ollama with `llama3.2:1b`, with a deterministic fallback when the model is unavailable
- **Database-Backed Intelligence** — agents operate on live application data
- **Multi-Tenant Architecture** — university data is isolated through `tenant_id`
- **JWT Authentication** — protected API routes with role-aware access
- **Audit Trail** — agent executions are persisted for traceability
- **Analytics Dashboard** — visual reporting for platform activity
- **Automated Testing** — 12 pytest tests covering core API behavior

---

## Core Agents

| Agent | Responsibility |
|---|---|
| **AttendanceAgent** | Identifies students with attendance risk |
| **PolicyAgent** | Retrieves institutional policy thresholds and rules |
| **RiskAgent** | Analyzes academic risk using attendance and grades |
| **KnowledgeAgent** | Retrieves relevant institutional documents |

New agents can be added through the registry without changing the orchestrator flow.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI, SQLAlchemy |
| Frontend | React 19, Vite, Tailwind CSS |
| Charts | Recharts |
| Database | SQLite (development), PostgreSQL (production path) |
| Authentication | JWT, bcrypt |
| LLM | Ollama (`llama3.2:1b`) |
| Testing | pytest, httpx |

---

## Application Areas

The current interface includes:

- Dashboard
- AI Command Center
- Agent Registry
- Students Directory
- Courses Directory
- Knowledge Base
- Audit Logs
- Analytics
- Login and Registration

---

## Screenshots

The screenshots below follow the **actual application flow** rather than the upload/file-name order: authentication → dashboard → AI workflows → core university modules → audit and analytics.

### 1. Authentication

#### Login

<img src="docs/Screenshot%20(1017).png" alt="UniNexus AI Login" width="100%">

#### Registration

<img src="docs/Screenshot%20(1019).png" alt="UniNexus AI Registration" width="100%">

#### Registration — Role Selection

<img src="docs/Screenshot%20(1013).png" alt="UniNexus AI registration role selection" width="100%">

#### Registration — Validation

<img src="docs/Screenshot%20(1020).png" alt="UniNexus AI registration validation" width="100%">

### 2. Dashboard

<img src="docs/Screenshot%20(1018).png" alt="UniNexus AI Dashboard" width="100%">

### 3. AI Command Center — Agentic Workflow

#### Task Ready

<img src="docs/Screenshot%20(1007).png" alt="AI Command Center task input" width="100%">

#### Task Executing

<img src="docs/Screenshot%20(1008).png" alt="AI Command Center executing workflow" width="100%">

#### Orchestrated Execution Plan

<img src="docs/Screenshot%20(1009).png" alt="AI Command Center execution plan with RiskAgent" width="100%">

#### RiskAgent Results

<img src="docs/Screenshot%20(1010).png" alt="RiskAgent execution results" width="100%">

### 4. AI Command Center — Knowledge + Policy Workflow

#### Attendance Rules Request

<img src="docs/Screenshot%20(978).png" alt="Knowledge and policy workflow request" width="100%">

#### KnowledgeAgent Results

<img src="docs/Screenshot%20(979).png" alt="KnowledgeAgent results" width="100%">

#### PolicyAgent Results

<img src="docs/Screenshot%20(980).png" alt="PolicyAgent results" width="100%">

### 5. AI Command Center — Attendance Workflow

#### Low-Attendance Request and Plan

<img src="docs/Screenshot%20(966).png" alt="Attendance workflow execution plan" width="100%">

#### AttendanceAgent Results

<img src="docs/Screenshot%20(967).png" alt="AttendanceAgent results" width="100%">

### 6. University Management Modules

#### AI Agent Registry

<img src="docs/Screenshot%20(985).png" alt="AI Agent Registry" width="100%">

#### Students

<img src="docs/Screenshot%20(986).png" alt="Students directory" width="100%">

#### Courses

<img src="docs/Screenshot%20(987).png" alt="Courses directory" width="100%">

#### Knowledge Base

<img src="docs/Screenshot%20(988).png" alt="Knowledge Base" width="100%">

### 7. Audit & Analytics

#### Audit Logs

<img src="docs/Screenshot%20(989).png" alt="Audit Logs" width="100%">

#### Analytics Overview

<img src="docs/Screenshot%20(997).png" alt="Analytics overview" width="100%">

#### Analytics — Detailed Charts

<img src="docs/Screenshot%20(1000).png" alt="Analytics detailed charts" width="100%">

---

## Architecture

```text
React Frontend
    |
    | JWT-authenticated REST API
    v
FastAPI Backend
    |
    v
Orchestrator
    |
    +--> AttendanceAgent
    +--> PolicyAgent
    +--> RiskAgent
    +--> KnowledgeAgent
    |
    +--> SQLite / PostgreSQL
    |
    +--> Ollama (local LLM planning)
```

---

## Multi-Tenancy

Every sensitive domain model carries a `tenant_id`. API queries are scoped to the authenticated user's tenant so one university cannot read another university's application data.

## Authentication

- JWT access tokens
- Passwords hashed with bcrypt
- Protected API routes
- Frontend token handling through an Axios interceptor

## Audit Logging

Every agent execution is persisted with execution metadata, allowing the platform to expose an auditable history through the Audit Logs interface.

## Database

- **Development:** SQLite (`uninexus.db`)
- **Production path:** PostgreSQL using the same SQLAlchemy model layer

## LLM Integration

`backend/app/core/llm.py` wraps Ollama for local planning. The planner requests structured JSON output and falls back to deterministic keyword-based planning when Ollama is unavailable.

---

## Quick Start

### Backend

```powershell
cd F:\UniNexus-AI
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install fastapi "uvicorn[standard]" sqlalchemy pydantic-settings python-jose[cryptography] "passlib[bcrypt]" python-multipart email-validator ollama pytest httpx
python seed_demo_data.py
python seed_documents.py
uvicorn backend.app.main:app --reload
```

Backend: `http://127.0.0.1:8000`  
API docs: `http://127.0.0.1:8000/docs`

### Frontend

```powershell
cd frontend
npm install
npm run dev
```

Frontend: `http://localhost:5173`

### Local LLM

```powershell
ollama pull llama3.2:1b
```

Ollama is optional for the demo flow because the orchestrator includes a deterministic fallback.

---

## Testing

```powershell
.\.venv\Scripts\Activate.ps1
python -m pytest tests/ -v
```

Expected: **12 passing tests**

---

## Project Structure

```text
UniNexus-AI/
├── backend/app/
│   ├── agents/       # orchestrator, base agent, specialized agents, registry
│   ├── api/          # authentication, agents, stats, academic, analytics
│   ├── core/         # configuration, database, security, LLM wrapper
│   ├── models/       # SQLAlchemy models
│   ├── schemas/      # Pydantic schemas
│   └── main.py       # FastAPI entry point
├── frontend/src/
│   ├── api/          # Axios client
│   ├── components/   # reusable UI components
│   └── pages/        # application pages
├── tests/             # pytest suite
├── docs/              # project documentation
├── seed_demo_data.py
├── seed_documents.py
├── .env.example
├── .gitignore
├── LICENSE
└── README.md
```

---

## Honest Limitations

This repository is a **portfolio demonstration**, not production university software.

- No live integration with a real university LMS, SIS, ERP, or portal yet
- Knowledge retrieval is currently keyword-based rather than vector-semantic RAG
- Human approval UI is not implemented yet
- SQLite is used for development
- The local LLM is intentionally small to keep the project free and lightweight

---

## Roadmap

- Semantic RAG with vector embeddings
- Human approval workflows
- Email and in-app notifications
- LMS connectors (Moodle, Canvas via LTI)
- Docker Compose deployment
- Production-grade university integrations

---

## License

MIT

**Built by ZARAK KHAN — UniNexus AI, 2026**
