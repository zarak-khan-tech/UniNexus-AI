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
