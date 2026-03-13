# Environment Variables

Example layouts.

## Web / Frontend (.env.example)
```dotenv
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_SUPABASE_URL=YOUR_SUPABASE_PROJECT_URL
NEXT_PUBLIC_SUPABASE_ANON_KEY=YOUR_SUPABASE_ANON_KEY
```

## Backend / API (.env.example)
```dotenv
# Core App
APP_ENV=development
SECRET_KEY=long-random-string
CORS_ORIGINS=["http://localhost:3000"]

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/sales_agent

# AI / LLM
OPENAI_API_KEY=sk-xxxx
LANGCHAIN_TRACING_V2=true 
LANGCHAIN_API_KEY=ls__xxxx

# Worker / Background Queues
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/1

# Optional Provider Integrations
# CLEARBIT_API_KEY=xxxx
# SENDGRID_API_KEY=xxxx
```
