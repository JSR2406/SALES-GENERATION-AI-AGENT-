# Production Launch Checklist

Follow these exact steps to ensure a safe, secure, and fully operational deployment of the Autonomous B2B Sales Agent.

---

## 🏗️ 1. Infrastructure Preparation
- [ ] **Provision PostgreSQL Data**
  - Use Render, Supabase, or AWS RDS.
  - Set strong passwords.
- [ ] **Configure Domain Names**
  - Frontend: Ensure domain is connected on Vercel (e.g., `app.mycompany.com`).
  - Backend: Ensure custom domain is connected on PaaS (e.g., `api.mycompany.com`).
  
## 🔐 2. Secret & Environment Variable Management
*Never hardcode passwords or API keys. Update via CI or dashboard.*

- [ ] **Backend Secrets (Render/Railway)**
  - `DATABASE_URL` (Check it includes `postgresql+asyncpg://`)
  - `SECRET_KEY` (Generate via `openssl rand -hex 32`)
  - `ANTHROPIC_API_KEY` (Set Claude 3.5 Sonnet limits)
  - `BACKEND_CORS_ORIGINS` (Must strictly match Vercel origin: `["https://app.mycompany.com"]`)
- [ ] **Frontend Secrets (Vercel)**
  - `VITE_API_BASE_URL` (Must strictly match backend URL: `https://api.mycompany.com/api/v1`)

## 🚢 3. Deployment Validation
- [ ] **Apply Migrations**
  - Render should automatically run `alembic upgrade head` via the `Dockerfile.prod` entry. Check the logs.
- [ ] **Service Health Check**
  - Verify `https://api.mycompany.com/api/v1/health` returns `200 OK`.
- [ ] **Frontend CORS Check**
  - Login via Vercel frontend. Ensure no preflight or `403` CORS errors appear in Network dev tools.

## 🔎 4. LangGraph Edge Case QA
- [ ] **Background Task Check**
  - Fire a "Test Campaign". Verify background worker spins up.
  - Check Render logs for Claude responses and parsing success.
- [ ] **Mock Provider Transition**
  - If mock providers were used, fully swap to real external scraping and email tools and re-test pipeline natively.

## 🚀 5. Final Handoff
- [ ] Back up database configurations locally.
- [ ] Notify stakeholders & document next limitations (e.g., auto-scale policies needed beyond 500 leads/day).
