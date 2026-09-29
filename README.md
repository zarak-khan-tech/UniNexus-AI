# UniNexus AI

**Autonomous Multi-Agent University Intelligence Platform**

Built by **ZARAK KHAN**

[![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-19-61DAFB?logo=react&logoColor=black)](https://react.dev)
[![Tests](https://img.shields.io/badge/tests-12%20passing-brightgreen)](tests/)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

---

## Overview

UniNexus AI is a modular, multi-tenant AI platform that operates as an intelligent layer over existing university ecosystems. It is **not a chatbot** - it is a genuine multi-agent system with real reasoning, real tools, real memory, and real safety controls.

**Core capabilities:**

- **Real agentic reasoning** - the LLM thinks, calls tools, and produces grounded answers (verified, no hallucination)
- **7 executable tools** with permission levels (READ / WRITE_LOW / WRITE_HIGH)
- **Human approval workflow** - high-risk actions are intercepted and held for admin review
- **Semantic RAG** over 20 university documents using vector embeddings (cosine similarity)
- **Multi-turn conversation memory** - pronoun resolution, continuity, session persistence
- **4 specialized agents** - Attendance, Policy, Risk, Knowledge
- **Event-driven workflows** - trigger -> action automation rules
- **Notification system** - bell icon + full page + hooks in every core flow
- **Multi-provider LLM gateway** - Groq -> Gemini -> Ollama automatic fallback
- **JWT auth, multi-tenancy, full audit trail**

---

## Screenshots

### AI Command Center - Real reasoning with tool-call trace

![Command Center](docs/screenshots/command-center.png)

*The reasoning loop shows every tool call, its arguments, and its result - fully auditable.*

### Dashboard - Live institutional snapshot

![Dashboard](docs/screenshots/dashboard.png)

*More screenshots in [docs/screenshots/](docs/screenshots/).*

---

## What Makes This Different

Most "AI" projects are wrappers around a single API call. This is a real system:

| Feature | UniNexus AI | Typical demo |
|---|---|---|
| LLM planning | Multi-step tool-calling | Single prompt |
| Grounding | Tool results only, cited | Hallucinates |
| Memory | Multi-turn, persistent | Stateless |
| Tools | 7 with permissions | No tools |
| Safety | Human approval for high-risk | None |
| RAG | Vector embeddings | Keyword search |
| Fallback | Groq -> Gemini -> Ollama | Single provider |
| Automation | Event-driven workflows | Manual only |
---

## Architecture

The system has three main layers:

**Frontend (React + Vite)**
- Dashboard, Command Center, Workflows, Approvals, Tools, Agents, Notifications, Analytics, Students, Courses, Knowledge Base, Audit Logs
- Axios client with JWT interceptor
- Polling for notifications every 30s

**Backend (FastAPI)**
- Reasoning Loop: LLM plans -> calls tools -> observes -> repeats or answers
- Tool Registry (7 tools with READ / WRITE_LOW / WRITE_HIGH permissions)
- Workflow Engine: trigger -> evaluate -> action -> notify
- Notification Service: bell + page + hooks in approval and workflow flows
- Approval Engine: WRITE_HIGH actions intercepted and held for human review
- LLM Gateway: Groq -> Gemini -> Ollama automatic fallback

**Data Layer**
- SQLite in dev, PostgreSQL path for prod
- SQLAlchemy ORM
- numpy + pickle vector store for semantic RAG
- 20 university documents embedded with nomic-embed-text

---

## Features

### Agentic Core
- Reasoning loop with tool calling (max 5 iterations)
- Multi-turn memory with pronoun resolution
- Session persistence (survives browser refresh)
- Anti-hallucination enforcement (strict grounding)
- Automatic retry on tool-call misbehavior
- Multi-provider LLM gateway with fallback chain

### Tools (7)

| Tool | Permission | Purpose |
|------|-----------|---------|
| student_lookup | READ | Find students by name/number/email |
| list_students | READ | List all students |
| attendance_query | READ | Find low-attendance students |
| list_enrollments | READ | Get all enrollments + grades |
| semantic_search | READ | Vector search over documents |
| send_student_notification | WRITE_LOW | Auto-executes |
| update_student_grade | WRITE_HIGH | Requires admin approval |

### Human-in-the-Loop
- Approval queue for high-risk actions
- Approve/Decline UI with friendly summaries
- Automatic notification on approval/rejection
- Full audit trail per approval

### Automation
- Event-driven workflows (trigger + action)
- Friendly result cards (no raw JSON)
- Run-now and run-all controls
- Pause/resume workflows

### Notifications
- Bell icon with unread badge
- Dropdown with recent 8
- Full page with filters (all/unread/read)
- Polling every 30s
- Hooks in approval flow + workflows

---

## Tech Stack

| Layer | Choice | Why |
|-------|--------|-----|
| Backend | FastAPI | Async, auto OpenAPI docs |
| Frontend | React 19 + Vite | Fast HMR, component model |
| Styling | Tailwind v4 | Utility-first |
| Charts | Recharts | Declarative, no external deps |
| Database | SQLite (dev) / PostgreSQL (prod) | Zero-setup dev |
| ORM | SQLAlchemy 2.x | Mature, well-documented |
| Auth | JWT + bcrypt | Standard, stateless |
| LLM (primary) | Groq (openai/gpt-oss-120b) | Free, ultra-fast |
| LLM (fallback) | Google Gemini | Free tier |
| LLM (offline) | Ollama | Fully local, no internet |
| Embeddings | Ollama (nomic-embed-text) | Local, 274 MB |
| Vector store | numpy + pickle | Zero-dependency |
| Tests | pytest + httpx | Fast, idiomatic |

---

## Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+
- Ollama (optional but recommended)

### 1. Backend
# 🎯 Bilkul — Aap Ka Plan Bilkul Sahi Hai

Aap ka idea **bahut acha hai**. Chalo main clearly batata hoon.

## Aap Ka Plan — Yes, Ye Karo

1. **Poori chat + screenshots ek Word doc mein paste karo** ✅
2. **ChatGPT ko do** — wo professional README likh dega ✅
3. **ChatGPT tumhari GitHub se connected hai** — wo direct repo dekh lega ✅
4. **Meri taraf se prompt bhi de deta hoon** (neeche) ✅

Ye approach **faayde ka** hai kyunke:
- ChatGPT fresh perspective dega
- Wo literally GitHub pe files dekh sakta hai
- PowerShell ke heredoc issues se pareshaan nahi honge

---

## 📝 Prompt Jo Aap ChatGPT Ko Dena

Ye Word doc ke start mein likh do:

```
I'm sharing a complete chat log of a project I've been building with 
another AI assistant. The project is called UniNexus AI — a multi-agent 
university intelligence platform. The backend is FastAPI + SQLite, 
frontend is React 19 + Vite + Tailwind v4, and it uses Groq/Gemini/Ollama 
for LLM, plus semantic RAG over 20 documents.

You are connected to my GitHub repo: https://github.com/zarak-khan-tech/UniNexus-AI

Please write me a PROFESSIONAL, PORTFOLIO-GRADE README.md that:
1. Opens with a compelling one-paragraph description of what UniNexus AI is
2. Includes a Features section, organized by category
3. Has an Architecture section (text-based diagram is fine)
4. Lists the full Tech Stack in a table with reasons
5. Has a "What Makes This Different" section comparing to typical AI demos
6. Includes honest Limitations (no fake claims)
7. Has a Roadmap (completed + planned)
8. Has clean Getting Started instructions
9. Includes the 2 screenshots I've attached
10. Uses badges, proper markdown tables, and clean formatting

Tone: confident but honest. Portfolio piece for a job application.

After the README, also tell me:
- What to do about PRD Section B (Docker setup) — should I skip it?
- What to do about PRD Section C (documentation/testing) — is it covered?
```

**Word doc ke end mein attach karo:**
- 2 screenshots (`command-center.png` and `dashboard.png`)
- PRD ka wo section jismein B and C mentioned hain

---

## ✅ Par — Ek Chhota Kaam Khud Kar Lo Abhi

README abhi **121 lines** hai — kuch missing hai. ChatGPT ko dene se pehle ye 2-minute ka kaam karo. Chahe ChatGPT baad mein rewrite kare, abhi ke liye complete hona chahiye.

### Sirf Ek Last Notepad Paste

```powershell
Set-Location F:\UniNexus-AI
notepad README.md
```

Notepad khulega. `Ctrl+End` dabao (aakhir mein cursor jayega). Phir ye paste karo:

```
cd F:\UniNexus-AI
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install fastapi "uvicorn[standard]" sqlalchemy pydantic-settings python-jose[cryptography] "passlib[bcrypt]" python-multipart email-validator ollama groq google-genai pytest httpx requests numpy

python seed_demo_data.py
python seed_documents.py
python seed_rich_documents.py
python ingest_documents.py

uvicorn backend.app.main:app --reload
```

Backend: http://127.0.0.1:8000 · Docs: http://127.0.0.1:8000/docs

### 2. Frontend

```
cd frontend
npm install
npm run dev
```

Frontend: http://localhost:5173

### 3. Local LLM + Embeddings

```
ollama pull llama3.2:1b
ollama pull llama3.2
ollama pull nomic-embed-text
```

### 4. Default credentials

- Email: admin@demo.university.edu
- Password: securepassword123
- Tenant ID: 1

### 5. Configure LLM providers (.env)

```
LLM_PROVIDER=groq
GROQ_API_KEY=gsk_...
GEMINI_API_KEY=AQ...
OLLAMA_MODEL=llama3.2:1b
```

---

## Testing

```
.\.venv\Scripts\Activate.ps1
python -m pytest tests/ -v
```

Expected: 12 passed.

---

## Roadmap

- [x] Multi-agent orchestration with LLM planning
- [x] Multi-tenant database schema
- [x] JWT authentication
- [x] Tool system with permissions
- [x] Semantic RAG
- [x] Multi-turn reasoning memory
- [x] Human approval workflow
- [x] Notification system
- [x] Event-driven workflows
- [x] Audit trail + tests
- [ ] Docker Compose for one-command deploy
- [ ] LMS connectors (Moodle, Canvas)
- [ ] Role-based UI filtering

---

## Honest Limitations

Portfolio-grade demo, not production software:

- No real university integration (Demo University seeded locally)
- Small local LLM fallback (Groq is primary)
- Keyword-boosted embeddings (good for demo)
- SQLite in dev (PostgreSQL for prod)
- In-memory vector store

---

## License

MIT. See LICENSE for details.

---

**Built by ZARAK KHAN** · UniNexus AI · 2026
```
