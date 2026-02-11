# AI-Powered Business Intelligence Platform (Arabic-First)

Production-style full-stack platform for multi-tenant BI + RAG workflows.

## Stack

- Backend: Django 5, DRF, PostgreSQL, Redis, Celery, JWT, drf-spectacular
- Frontend: React + TypeScript + Vite, Tailwind, TanStack Query, Recharts
- AI: Pluggable provider abstraction (OpenAI default), embeddings + retrieval + citation synthesis

## Architecture

### Persistent relational layer (PostgreSQL)
- Organizations, memberships, documents, chunks, chat sessions/messages, KPI datasets/records, audit logs
- Strong organization isolation via queryset filtering and membership checks

### Fast in-memory layer (Redis)
- API response caching (RAG answers)
- Session/chat hot data cache
- Simple rate-limiting counters
- Celery broker and result backend

### Document intelligence pipeline (Celery)
1. `parse_document`: extract text/tables from PDF/DOCX/CSV/XLSX
2. `chunk_document`: Arabic-aware sentence split + overlap chunking
3. `embed_document`: generate embeddings for each chunk

### RAG flow
1. Embed user query
2. Retrieve top-k relevant chunks (org-scoped)
3. Generate answer in Arabic/English
4. Return citations: document name + snippet + page (when available)

## Repository Structure

- `docker-compose.yml`
- `.env.example`
- `backend/`
- `frontend/`

## Environment Variables

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Key variables:

- Database: `POSTGRES_*`
- Django: `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, `DJANGO_ALLOWED_HOSTS`, `DJANGO_CORS_ALLOWED_ORIGINS`
- Locale: `DJANGO_TIME_ZONE=Asia/Riyadh`, `DJANGO_LANGUAGE_CODE=ar-sa`
- Redis/Celery: `REDIS_URL`, `CELERY_BROKER_URL`, `CELERY_RESULT_BACKEND`
- AI: `OPENAI_API_KEY`, `OPENAI_CHAT_MODEL`, `OPENAI_EMBEDDING_MODEL`
- Frontend: `VITE_API_BASE_URL`

## Docker Usage

```bash
docker compose up --build
```

Services:
- `postgres`
- `redis`
- `backend` (Django + Celery worker)
- `frontend` (Vite dev server)

Backend API base URL: `http://localhost:8000/api`  
Frontend URL: `http://localhost:5173`

## Auth & Core APIs

- `POST /api/auth/login`
- `POST /api/auth/refresh`
- `GET /api/auth/me`
- `GET|POST /api/orgs`
- `GET|POST /api/documents`
- `GET|POST /api/chat/sessions`
- `POST /api/chat/ask`
- `GET|POST /api/kpi/datasets`
- `GET /api/kpi/analytics`
- `GET /api/audit`

OpenAPI docs:
- `GET /api/schema`
- `GET /api/docs`

## Quick Demo Steps

1. Start stack with Docker Compose.
2. Login with seeded user:
   - username: `admin`
   - password: `admin12345`
3. Open dashboard:
   - see seeded Saudi branch data (Riyadh, Dammam, Jeddah)
   - upload additional CSV/XLSX for KPI analytics
4. Upload PDF/DOCX files in Documents page and wait for status `ready`.
5. Ask Arabic questions in Chat page, for example:
   - `ما هي أبرز المبيعات حسب الفرع؟`
6. Review audit events in Audit Logs page.

## Security & Quality Notes

- JWT authentication with refresh rotation
- RBAC via membership roles (`admin`, `manager`, `analyst`, `viewer`)
- Multi-tenant data isolation per organization
- Input validation for uploaded files and organization access
- Redis-backed rate limiting for login/chat operations
- Structured audit logging for logins/uploads/AI usage

## Notes

- If `OPENAI_API_KEY` is unset, the app uses a deterministic fallback embedding/response mode so the pipeline still works end-to-end.
- In this scaffold, migrations are auto-generated at container startup (`makemigrations && migrate`) to simplify first-run setup.

## Code Review Workflow (CodeRabbit)

### 1) Install and connect CodeRabbit
- Install the CodeRabbit GitHub App on this repository.
- Ensure repository access includes `AhmedRawaf/ai-business-intelligence-platform`.

### 2) Use PR-based review (recommended)
CodeRabbit reviews PR diffs, so for "whole project" review use a batch strategy:

1. PR A: backend config + auth + orgs
2. PR B: documents + celery + AI/RAG
3. PR C: KPI + frontend dashboard/chat/docs/audit
4. PR D: hardening (tests, security, cleanup)

### 3) Trigger and guide review
- Open PR and wait for automatic review.
- Add a comment like `/review` for a fresh pass.
- Use the PR template in `.github/pull_request_template.md` to focus review on risk-heavy areas.

### 4) Project defaults
- `.coderabbit.yaml` is preconfigured to:
  - focus on source code and key config files,
  - ignore generated/noisy paths,
  - provide high-level summary + detailed walkthrough status.
