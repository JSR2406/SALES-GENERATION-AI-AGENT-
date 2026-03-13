from typing import Dict, Any, cast
from app.core.supabase import supabase  # type: ignore
from app.agents.workflow import sales_agent_executor, AgentState  # type: ignore

class AgentService:
    @staticmethod
    async def run_campaign_pipeline(campaign_id: str):
        """
        Runs the full LangGraph pipeline for a specific campaign and saves results to Supabase.
        """
        # 1. Fetch Campaign Context from Supabase
        response = supabase.table("campaigns").select("*").eq("id", campaign_id).execute()
        if not response.data:
            print(f"Campaign {campaign_id} not found.")
            return

        campaign = response.data[0]
        
        # 2. Initialize State
        initial_state: dict[str, Any] = {
            "campaign_id": campaign_id,
            "campaign_context": campaign,
            "leads": [],
            "status": "started",
            "errors": []
        }

        # 3. Execute Graph and Stream Updates for Audit Logs
        import json
        final_state = initial_state
        async for events in sales_agent_executor.astream(initial_state, stream_mode="updates"):
            for node_name, state_update in events.items():
                print(f"--- Node Executed: {node_name} ---")
                
                # Write to Agent Audit Logs in Supabase
                try:
                    # Clean up data slightly for JSON logging
                    log_details = {
                        "leads_count": len(state_update.get("leads", [])),
                        "status": state_update.get("status", "unknown")
                    }
                    supabase.table("agent_logs").insert({
                        "campaign_id": campaign_id,
                        "node": node_name,
                        "status": "completed",
                        "details": log_details
                    }).execute()
                except Exception as e:
                    print(f"Failed to log to agent_logs: {e}")
                    
                # Continue accumulating the final state
                final_state = {**final_state, **state_update}

        # 4. Save Results to Supabase (Leads and OutreachMessages)
        for lead_data in final_state.get("leads", []):
            # Insert lead
            lead_resp = supabase.table("leads").insert({
                "campaign_id": campaign_id,
                "full_name": lead_data["full_name"],
                "company_name": lead_data["company_name"],
                "qualification_score": lead_data["qualification_score"],
                "qualification_reason": lead_data["qualification_reason"],
                "status": "draft_ready"
            }).execute()

            if lead_resp.data:
                lead_id = lead_resp.data[0]["id"]
                # Insert outreach message
                supabase.table("outreach_messages").insert({
                    "campaign_id": campaign_id,
                    "lead_id": lead_id,
                    "subject": lead_data["email_subject"],
                    "body": lead_data["email_body"],
                    "status": "pending_approval"
                }).execute()

        print(f"--- Pipeline completed for campaign {campaign_id} ---")
        return final_state
