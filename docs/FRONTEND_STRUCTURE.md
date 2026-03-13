# Frontend Structure

## Principles
- Built with **Next.js 14 (App Router)**.
- Tailored for a modern B2B SaaS feel with minimalistic empty states, loaders, and toast feedbacks.
- Uses **shadcn/ui** primitives + **Tailwind CSS**.

## Structure
```text
frontend/
  src/
    app/
      (auth)/                  # Auth layout & sign-in/up
      (dashboard)/             # Main protected wrapper
      page.tsx                 # Landing Page
      layout.tsx               # Root Layout
    components/
      ui/                      # shadcn primitives
      shared/                  # Layout shells, navbars, sidebars
    features/
      auth/                    # login forms
      dashboard/               # overview cards, graphs
      campaigns/               # build & detail flows
      leads/                   # table & slide-over displays
      approvals/               # approval pipeline lists
      analytics/               # metric summaries
    lib/                       # utils, validators, context blocks
    hooks/                     # logic encapsulation
    services/                  # api fetchers / endpoints
    types/                     # global TS types
    tests/                     # component/e2e specs
```

## Key Modules
1. **Approval Queue View**: Side-by-side or stacked view. Shows lead details next to the generated LLM draft. Action buttons: Appove, Reject, Edit, Regenerate.
2. **Campaign Builder**: Step-by-step or seamless vertical form. High validation via Zod.
