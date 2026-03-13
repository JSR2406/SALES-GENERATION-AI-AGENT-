from langgraph.graph import StateGraph, END
from app.agents.state import AgentState
from app.agents.nodes import (
    supervisor_node,
    discover_leads_node,
    enrich_lead_node,
    qualify_lead_node,
    draft_email_node,
    approval_gate_node,
    send_email_node,
    failure_handler_node
)

def build_graph():
    """Builds the deterministic state machine for the Sales Agent."""
    workflow = StateGraph(AgentState)
    
    # 1. Add Nodes
    workflow.add_node("supervisor", supervisor_node)
    workflow.add_node("discover_leads", discover_leads_node)
    workflow.add_node("enrich_lead", enrich_lead_node)
    workflow.add_node("qualify_lead", qualify_lead_node)
    workflow.add_node("draft_email", draft_email_node)
    workflow.add_node("approval_gate", approval_gate_node)
    workflow.add_node("send_email", send_email_node)
    workflow.add_node("failure", failure_handler_node)
    
    # 2. Add routing logic from Supervisor
    workflow.set_entry_point("supervisor")
    
    workflow.add_conditional_edges(
        "supervisor",
        # Custom routing lambda based on internal node logic
        lambda state: state.get("next_action"),
        {
            "discover_leads": "discover_leads",
            "enrich_lead": "enrich_lead",
            "qualify_lead": "qualify_lead",
            "draft_email": "draft_email",
            "approval_gate": "approval_gate",
            "send_email": "send_email",
            "failure": "failure",
            "end": END
        }
    )
    
    # 3. All child nodes simply return control to supervisor
    workflow.add_edge("discover_leads", "supervisor")
    workflow.add_edge("enrich_lead", "supervisor")
    workflow.add_edge("qualify_lead", "supervisor")
    workflow.add_edge("draft_email", "supervisor")
    workflow.add_edge("send_email", "supervisor")
    
    # 4. Terminal Nodes
    workflow.add_edge("approval_gate", END) # Pauses completely
    workflow.add_edge("failure", END)
    
    # Compile with persistence if using memory checkpointer (e.g., Postgres checkpointer in production)
    app = workflow.compile()
    return app
