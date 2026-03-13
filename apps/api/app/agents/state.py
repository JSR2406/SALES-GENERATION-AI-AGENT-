# apps/api/app/agents/state.py
from typing import TypedDict, Optional, List, Dict, Any, Annotated
import operator
from uuid import UUID

def reduce_list(left: list, right: list) -> list:
    if not right:
        return left
    if not left:
        return right
    return left + right

class AgentState(TypedDict):
    # Context
    campaign_id: UUID
    user_id: UUID
    
    # Campaign configuration (readonly within the graph)
    target_icp: Dict[str, Any]
    user_value_prop: str
    offer_summary: str
    sending_mode: str # 'manual_approval' or 'auto_send'
    
    # Execution Tracking
    current_lead_data: Optional[Dict[str, Any]]
    qualification_result: Optional[Dict[str, Any]]
    drafted_email: Optional[Dict[str, Any]]
    
    # Control flags
    routing_status: str # determines path
    
    # Audit trail
    errors: Annotated[List[str], reduce_list]
