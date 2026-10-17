<div align="center">

# 🏛️ UniNexus AI
**Autonomous Multi-Agent University Intelligence Platform**

[![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-19-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev)
[![TailwindCSS](https://img.shields.io/badge/Tailwind_v4-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org/)
[![Tests](https://img.shields.io/badge/Tests-53_Passing-brightgreen?style=for-the-badge)](#)

Built by **ZARAK KHAN** — A production-grade portfolio project exploring agentic AI, RAG, and human-in-the-loop workflows.

</div>


## 🚀 Quick Showcase

Don't want to read the code? **See the platform in action.**
Click the button below to view all high-resolution screenshots of the AI Command Center, Workflows, and Audit Logs.

<div align="center">

[![View Project Showcase](https://img.shields.io/badge/🖼️_VIEW_PROJECT_SHOWCASE-FFD700?style=for-the-badge&logoColor=black&labelColor=black)](SHOWCASE.md)

</div>


## 🧠 What is UniNexus AI?

UniNexus AI is not just a chatbot. It is a **modular, multi-tenant AI platform** that acts as an intelligent layer over a university ecosystem. 

Instead of treating an LLM as a standalone tool, UniNexus AI gives the model **controlled access** to institutional data and actions through a strict reasoning loop.

> ⚠️ **Honest Positioning:** This is an educational/portfolio architecture. It uses locally seeded demo data and does not connect to real live university systems without proper credentials.


## ✨ Core Capabilities

*   🧠 **Agentic Reasoning Loop:** Multi-step planning with tool execution, memory, and source citations.
*   🛡️ **Safety & Hallucination Guard:** Rejects answers if no evidence is found. Detects prompt injection.
*   🛠️ **Dynamic Tool Registry:** 7 permission-based tools (READ, WRITE_LOW, WRITE_HIGH) with DB-driven toggles.
*   🤝 **Human-in-the-Loop:** High-risk actions (e.g., changing grades) are intercepted and queued for Admin approval.
*   📚 **Advanced RAG Pipeline:** Vector-based semantic search with evidence-quality filtering (Strong/Weak/None).
*   🔄 **Event-Driven Workflows:** Auto-triggers notifications when events (like Document Uploads) occur.
*   🔒 **Multi-Tenant Isolation:** Strict RBAC (Admin, Faculty, Student) with 8 isolated tenant test scenarios.


## 🏗️ Architecture Stack

| Layer | Technologies Used |
| :--- | :--- |
| **Backend** | Python, FastAPI, SQLAlchemy, Pytest |
| **Frontend** | React 19, Vite, Tailwind CSS v4, Recharts |
| **AI / LLM** | Groq (Primary), Google Gemini (Fallback), Ollama (Local) |
| **Embeddings** | Ollama (`nomic-embed-text`), NumPy Vector Store |
| **Security** | JWT Authentication, Passlib (Bcrypt), Rate Limiting |


## ⚙️ Quick Start Guide

### 1. Backend Setup
```bash
git clone https://github.com/zarak-khan-tech/UniNexus-AI.git
cd UniNexus-AI
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Seed demo data
python seed_demo_data.py
python seed_rich_documents.py
python ingest_documents.py

# Run Backend
uvicorn backend.app.main:app --reload
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### 🔑 Default Credentials
- **Email:** `admin@demo.university.edu`
- **Password:** `securepassword123`


## 🧪 Testing

To ensure reliability and multi-tenant isolation, run the test suite:
```bash
$env:PYTHONPATH = "F:\UniNexus-AI"
python -m pytest tests/ -v
```
*Currently passing: **53 automated tests**.*


## 📄 License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
