# Agent Workflow

LangGraph Architecture for deterministic state-based transitions.

## Agent State Schema
- run_id (str)
- campaign_id (UUID)
- user_id (UUID)
- current_step (str)
- campaign_data (dict)
- lead_query (dict)
- discovered_leads (list)
- current_lead (dict)
- enrichment_context (str)
- qualification_result (dict)
- draft_email (dict)
- draft_subject (str)
- personalization_notes (str)
- approval_required (bool)
- send_decision (bool)
- reply_scan_result (dict)
- errors (list)
- logs (list)
- next_action (str)

## Nodes
1. **supervisor_node**: Evaluates state and dictates the valid next node.
2. **discover_leads_node**: Connects to the lead provider to pull new leads.
3. **enrich_lead_node**: Captures deep contact/firmographic info based on simple details.
4. **qualify_lead_node**: Uses LLMs with specific ICP prompts to score the lead. Rejecting bad apples.
5. **draft_email_node**: Generates hyper-personalized subjects & messages minus hallucination.
6. **approval_gate_node**: Either pushes draft for manual UI view or pipes directly to send.
7. **send_email_node**: Calls EmailProvider abstraction logic and captures delivery.
8. **monitor_reply_node**: Detects thread responses, classifying intent for analytics.
9. **persist_activity_node**: Stores standard logs and actions into PG.
10. **failure_handler_node**: Captures soft and hard exceptions and routes state safely.
