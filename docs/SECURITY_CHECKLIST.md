# Security Checklist

1. [ ] Check JWT/Cookie logic for XSS and CSRF.
2. [ ] Rate Limiting on Lead generation / Send APIs.
3. [ ] Row-Level Security on PostgreSQL / Object Level permissions.
4. [ ] DB injections protected by SQLAlchemy abstractions.
5. [ ] Passwords stored using BCRYPT hashes.
6. [ ] Validations enforced STRICTLY through Zod/Pydantic schemas blocking bad payloads.
7. [ ] Hardcode safe parsing on Provider output logic (LLM data formats validated).
8. [ ] Do not output inner exception variables externally (Tracebacks omitted from Production API).
