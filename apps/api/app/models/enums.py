from enum import Enum

class CampaignStatus(str, Enum):
    draft = "draft"
    running = "running"
    paused = "paused"
    completed = "completed"
    failed = "failed"

class SendingMode(str, Enum):
    manual_approval = "manual_approval"
    auto_send = "auto_send"

class LeadStatus(str, Enum):
    discovered = "discovered"
    enriched = "enriched"
    qualified = "qualified"
    disqualified = "disqualified"
    drafting = "drafting"
    draft_ready = "draft_ready"
    approved = "approved"
    rejected = "rejected"
    contacted = "contacted"
    replied = "replied"

class OutreachStatus(str, Enum):
    drafting = "drafting"
    pending_approval = "pending_approval"
    approved = "approved"
    rejected = "rejected"
    sent = "sent"
    failed = "failed"
