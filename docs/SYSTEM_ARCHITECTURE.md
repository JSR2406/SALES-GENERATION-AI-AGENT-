# System Architecture

## Architecture Overview
The application is structured as a mono-repo.

```text
autonomous-b2b-sales-agent/
  apps/
    web/       # Next.js 14 frontend (App Router)
    api/       # Python FastAPI backend
  docs/        # Project documentation
  infra/       # Infrastructure and Docker configs
  .github/     # GitHub actions
```

## Backend Architecture (apps/api)
- `api/routes/`: FastAPI routers and endpoints.
- `core/`: Configurations, security, logging, and database abstractions.
- `models/`: SQLAlchemy (or SQLModel) core relational forms.
- `schemas/`: Pydantic validation schemas.
- `services/`: Core logic and abstractions.
- `providers/`: Mocks or actual connections for external systems (Email, Leads, Enrichment).
- `agents/`: LangGraph orchestrations using deterministic state management, nodes, and prompts.

## Frontend Architecture (apps/web)
- `app/`: Next.js app router structure.
- `components/`: UI components (shadcn/ui + custom).
- `features/`: Module specific blocks (dashboards, campaigns).
- `services/`: API hooks and data-fetching definitions.
- `hooks/`: Custom react hooks.
- `types/`: Shared TypeScript types aligned roughly with API responses.

## Sub-Systems
1. **LangGraph Agent Engine**: Executes specific step-driven processes for discovering, qualifying, drafting, and optionally sending emails.
2. **PostgreSQL + Supabase**: Hosts application transactional data with tight schema integrity.
3. **Background Jobs Engine**: Celery/Redis OR robust abstraction on top of FastAPI `BackgroundTasks`.
