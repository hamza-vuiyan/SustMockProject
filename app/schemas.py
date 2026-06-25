from pydantic import BaseModel
from typing import Optional

class TicketRequest(BaseModel):
    # Required fields
    ticket_id: str
    message: str
    
    # Optional fields (the test machine might not send these every time)
    channel: Optional[str] = None
    locale: Optional[str] = None


class TicketResponse(BaseModel):
    ticket_id: str
    case_type: str
    severity: str
    department: str
    agent_summary: str
    human_review_required: bool
    confidence: float