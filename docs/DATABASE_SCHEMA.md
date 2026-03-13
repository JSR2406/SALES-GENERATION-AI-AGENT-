# Database Schema

## `users`
- id (UUID, PK)
- email (String)
- hashed_password (String, nullable if OAuth)
- full_name (String)
- company_name (String)
- product_name (String)
- website (String)
- created_at, updated_at

## `user_profiles`
- id (UUID, PK)
- user_id (UUID, FK -> users.id)
- company_description (Text)
- default_value_proposition (Text)
- default_offer (Text)
- default_cta (Text)
- default_icp (Text)
- settings_json (JSONB)
- created_at, updated_at

## `campaigns`
- id (UUID, PK)
- user_id (UUID, FK -> users.id)
- campaign_name (String)
- target_industries (JSONB)
- target_locations (JSONB)
- target_company_size (String)
- target_job_titles (JSONB)
- target_keywords (JSONB)
- negative_keywords (JSONB)
- offer_summary (Text)
- product_description (Text)
- value_proposition (Text)
- call_to_action (Text)
- sending_mode (Enum: manual_approval, auto_send)
- max_leads (Int)
- max_daily_sends (Int)
- tone_preference (String)
- personalization_depth (String)
- follow_up_enabled (Boolean)
- follow_up_count (Int)
- follow_up_gap_days (Int)
- status (Enum: draft, running, paused, completed, failed)
- created_at, updated_at

## `leads`
- id (UUID, PK)
- campaign_id (UUID, FK -> campaigns.id)
- full_name (String), first_name (String), last_name (String)
- job_title (String)
- email (String)
- linkedin_url (String)
- company_name, company_domain, company_description
- source (String), source_url (String)
- raw_source_data_json (JSONB)
- enrichment_summary (Text)
- qualification_score (Float)
- qualification_reason (Text)
- status (Enum: discovered, enriched, qualified, rejected, draft_ready, approved, sent, replied, bounced, failed)
- created_at, updated_at

## `outreach_messages`
- id (UUID, PK)
- campaign_id (UUID, FK -> campaigns.id)
- lead_id (UUID, FK -> leads.id)
- subject, opening_line, body
- personalization_notes (Text)
- generation_inputs_json (JSONB), generation_output_json (JSONB)
- edited_by_user, approved_by_user (Boolean)
- sent_via (String), provider_message_id (String)
- delivery_status (String), reply_status (String)
- error_message (Text)
- sent_at, created_at, updated_at

## `replies`
- id (UUID, PK)
- outreach_message_id (UUID, FK -> outreach_messages.id)
- lead_id (UUID, FK -> leads.id)
- provider_thread_id (String)
- reply_text (Text)
- classification (Enum: interested, not_interested, ask_later, bounced, out_of_office, neutral)
- sentiment (String)
- extracted_intent (Text)
- received_at, created_at

## `activity_logs`
- id (UUID, PK)
- user_id (UUID, FK -> users.id)
- campaign_id, lead_id (UUIDs, nullable)
- action_type (String)
- action_status (String)
- summary (Text)
- metadata_json (JSONB)
- created_at

## `integrations`
- id (UUID, PK)
- user_id (UUID, FK -> users.id)
- provider_name (String)
- provider_type (String)
- encrypted_credentials_reference (String)
- status (String)
- created_at, updated_at
