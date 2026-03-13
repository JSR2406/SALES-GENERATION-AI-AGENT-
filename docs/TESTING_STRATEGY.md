# Testing Strategy

We cannot push unstable agent behaviour or poor API states.

## Backend (Pytest)
1. **Unit Tests (Services/Providers)**: Test data mappers and business logic layers completely isolated from DB layer using mocks.
2. **Agent Tests**: Test specific state transitions using LangGraph test utilities or manually instantiating state configurations. Ensure nodes handle transient errors correctly. Test LLM anti-hallucination guardrails via prompt eval suites.
3. **Integration Tests (API routes)**: End-to-end API hits against a `test_database` container ensuring DB persistence and status codes are met.

## Frontend (Vitest & Playwright)
1. **Component tests**: Isolate core complex forms (Campaign Builder, Approval Viewer) for edge cases.
2. **Form Validation Tests**: Verify Zod hooks catch bad boundary issues.
3. **E2E flows**: Mock the backend network. Simulate user logging in, creating a campaign, checking approval queue, and rejecting a draft.
