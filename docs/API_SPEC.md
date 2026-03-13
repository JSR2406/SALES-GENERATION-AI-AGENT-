# API Specification

## Authentication
- POST `/api/v1/auth/register`
- POST `/api/v1/auth/login`
- POST `/api/v1/auth/logout`
- GET `/api/v1/auth/me`

## Campaigns
- POST `/api/v1/campaigns`
- GET `/api/v1/campaigns`
- GET `/api/v1/campaigns/{campaign_id}`
- PATCH `/api/v1/campaigns/{campaign_id}`
- DELETE `/api/v1/campaigns/{campaign_id}`
- POST `/api/v1/campaigns/{campaign_id}/start`
- POST `/api/v1/campaigns/{campaign_id}/pause`
- POST `/api/v1/campaigns/{campaign_id}/resume`
- POST `/api/v1/campaigns/{campaign_id}/archive`

## Leads
- GET `/api/v1/campaigns/{campaign_id}/leads`
- GET `/api/v1/leads/{lead_id}`
- POST `/api/v1/leads/{lead_id}/approve`
- POST `/api/v1/leads/{lead_id}/reject`
- POST `/api/v1/leads/{lead_id}/regenerate-draft`
- PATCH `/api/v1/leads/{lead_id}/edit-draft`

## Outreach
- GET `/api/v1/campaigns/{campaign_id}/outreach`
- GET `/api/v1/outreach/{message_id}`
- POST `/api/v1/outreach/{message_id}/send`

## Analytics
- GET `/api/v1/dashboard/summary`
- GET `/api/v1/dashboard/recent-activity`
- GET `/api/v1/dashboard/campaign-performance`

## System
- GET `/health`
- GET `/ready`
