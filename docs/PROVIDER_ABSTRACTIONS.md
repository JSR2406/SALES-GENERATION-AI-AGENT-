# Provider Abstractions

Abstracting integrations ensures logic isolation.

## Interfaces
`ILeadProvider`: Fetch candidate leads (`discover_leads`).
`IEnrichmentProvider`: Gather detailed contact info (`enrich_lead`).
`IEmailProvider`: Issue send requests (`send_email`).
`IReplyProvider`: Parse inbound loops (`monitor_replies`).

## Mocks (Phase 1/2)
- `MockLeadProvider`
- `MockEnrichmentProvider`
- `MockEmailProvider`
- `MockReplyProvider`

## Real implementations (Planned)
- `ApifyLeadProvider` / `LinkedInProvider`
- `ClearbitEnrichmentProvider`
- `GmailProvider` / `OutlookProvider`
- `SendGridProvider`

**Rule**: The core system / agent nodes should ONLY call the Abstract Interfaces (Injection & Abstraction layer).
