# UniNexus AI Architecture

## Overview

UniNexus AI is a portfolio/educational multi-agent university intelligence platform built with React 19, FastAPI, SQLAlchemy/SQLite, a multi-provider LLM gateway, agent orchestration, RAG, approvals, workflows, notifications, audit logging, and analytics.

This is a serious portfolio/demo implementation. It is **not a production-certified university platform** and does not claim live access to private university LMS/SIS/ERP systems.

## High-Level Architecture

```text
React Frontend
  Dashboard · Command Center · Agents · Tools · RAG
  Approvals · Workflows · Notifications · Analytics · Audit
                 │ REST / JWT
                 ▼
FastAPI Backend
  Auth · Academic APIs · Agents · Tools · Workflows
  Approvals · Notifications · Analytics
        │                    │
        ▼                    ▼
Agent System             Data / Knowledge
Orchestrator             SQLAlchemy + SQLite
Agent Registry            Documents + Vector Store
Specialized Agents        Embeddings + Semantic Search
        │
        ▼
LLM Gateway
  Groq ↔ Gemini ↔ Ollama
  Runtime provider selection + fallback ordering
```

## Multi-Agent Flow

1. A user submits a natural-language request through the Command Center.
2. The orchestrator asks the configured LLM gateway whether the request needs a direct answer or an agent workflow.
3. The generated plan is validated against registered agents.
4. Specialized agents execute database or knowledge operations.
5. Sensitive write actions can pass through the approval layer.
6. Execution details are persisted for audit and analytics.
7. Structured results are returned to the frontend.

The LLM is not the only control layer: plans and agent names are validated, while deterministic application logic remains responsible for permissions and other critical controls.

## LLM Gateway

The gateway provides one interface for three providers:

| Provider | Role |
|---|---|
| **Groq** | Configurable remote inference provider |
| **Gemini** | Alternative remote inference provider |
| **Ollama** | Local/self-hosted provider |

`LLM_PROVIDER` selects the primary provider. The gateway tries the primary provider first and can continue through the other configured providers when one fails.

Models are environment-configurable. For local development, Ollama can use a model such as `llama3.2:3b`; the actual installed model depends on the developer machine.

## Specialized Agents

| Agent | Responsibility |
|---|---|
| **AttendanceAgent** | Finds students below an attendance threshold using database data |
| **PolicyAgent** | Returns institutional policy thresholds |
| **RiskAgent** | Identifies academic-risk students using attendance and grade data |
| **KnowledgeAgent** | Retrieves relevant institutional information from indexed documents |

Agents are registered centrally so the orchestrator can validate planned agent names before execution.

## Tool Registry

Agents use controlled tools instead of unrestricted database access.

Examples include attendance queries, enrollment lookup, academic data access, semantic document search, and controlled write operations.

Tools declare permission levels such as **READ**, **WRITE_LOW**, and **WRITE_HIGH**. Higher-risk operations can require human approval.

## Retrieval-Augmented Knowledge

The knowledge pipeline consists of:

1. Document ingestion
2. Text/chunk preparation
3. Embedding generation
4. Vector storage
5. Semantic retrieval
6. Agent-level use of retrieved context

The current vector-store implementation is lightweight and appropriate for a portfolio/demo environment rather than production-scale search infrastructure.

## Human-in-the-Loop

```text
AI / Agent
    ↓
Proposed Action
    ↓
Permission / Approval Gate
    ↓
Human Decision
    ├── Approve → Execute
    └── Decline → Stop / Record
```

Approval decisions are persisted and surfaced through the Approvals and Notifications interfaces.

## Workflow and Automation

The workflow engine supports condition-driven automation such as attendance-based checks. Workflow executions can generate notifications and execution records.

This demonstrates an autonomous-workflow architecture without claiming integration with real private university systems.

## Multi-Tenancy

Core university-scoped models carry a `tenant_id`, and authenticated requests use the current user's tenant context.

This demonstrates application-level tenant isolation; it is not a production security certification or independent security audit.

## Authentication and Security

- JWT-based authentication
- Password hashing with bcrypt
- Protected API routes
- Tenant-aware data access
- Environment-based configuration for secrets and API keys
- Approval controls for sensitive operations

A real deployment would additionally require production hardening for secrets, HTTPS, token storage, CORS, rate limiting, logging, authorization policies, backups, and monitoring.

## Database

Development uses SQLite through SQLAlchemy.

The project is optimized for local/demo use. A production deployment would require a production database, migrations, backup strategy, and operational monitoring.

## Testing

The repository contains pytest coverage for agent planning, tools, semantic search, memory/reasoning, approvals, notifications, workflows, and provider-related behavior.

The README should report an exact passing-test count only after the current suite has actually been executed.

## Deployment Direction

The original project requirements define Docker Compose as a later option after the application is stable.

For this portfolio version:

- **Docker is optional, not a prerequisite for local development.**
- Do not bundle large Ollama model files into an application image.
- A future Compose setup should separate application services from model hosting.
- Any containerized deployment should document environment variables, persistent storage, health checks, logs, rebuilds, and troubleshooting.
- Do not claim Docker deployment is working until it has actually been built and verified.

## Integration Boundaries

UniNexus AI does not provide universal plug-and-play access to private university systems. Real LMS/SIS/ERP integrations require institutional APIs, authentication, permissions, data mapping, security review, and vendor support.

The current system therefore focuses on a realistic multi-agent architecture, seeded/demo university data, document retrieval, approvals, workflows, and integration-ready boundaries.

---

**Built by ZARAK KHAN**
