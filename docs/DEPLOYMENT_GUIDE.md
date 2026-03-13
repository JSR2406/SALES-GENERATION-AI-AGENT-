# Deployment Guide

The app splits primarily between static frontend (Vercel) and dynamic worker/API backend (Render/Railway/GCP).

## Architecture Mapping
- **Database**: Supabase PostgreSQL (hosted DB).
- **Web App**: Vercel (Next.js automatically detected).
- **API Server**: Render/Railway Docker service or generic VM.
- **Worker Process**: Render background worker pulling celery jobs or identical FastAPI service running secondary CLI/Thread mode.
- **Redis**: Hosted instance for job queuing / websockets.

## Build steps (CI/GitHub Actions)
1. Lint (`flake8` / `eslint`)
2. Type check (`mypy` / `tsc`)
3. Test suite (`pytest` / `vitest`)
4. Build images if needed.

## Database Migrations
Handled explicitly via Alembic on the backend side prior to runtime booting.
`alembic upgrade head`
