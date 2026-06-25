from fastapi import FastAPI, HTTPException, status
# 1. Update this line to import the new response schema
from app.schemas import TicketRequest, TicketResponse 
# 2. Import your AI function
from app.ai_service import classify_ticket

app = FastAPI()

# 3. Hardcode the department rules so the AI doesn't have to guess 
DEPARTMENT_MAPPING = {
    "wrong_transfer": "dispute_resolution",
    "payment_failed": "payments_ops",
    "refund_request": "customer_support",
    "phishing_or_social_engineering": "fraud_risk",
    "other": "customer_support"
}

@app.post("/sort-ticket", response_model=TicketResponse, status_code=status.HTTP_200_OK)
async def sort_ticket(payload: TicketRequest):
    """
    Receives the incoming CRM ticket JSON, passes it to the AI,
    applies business logic, and returns the strict output schema.
    """
    current_id = payload.ticket_id
    customer_complaint = payload.message
    
    print(f"Processing ticket {current_id}...")
    
    try:
        # A. Hand the message to Gemini and wait for the JSON dictionary
        ai_data = await classify_ticket(customer_complaint)
        
        # --- THE RULE-BASED BACKUP PLAN ---
        # If the AI failed and returned an empty dict {}, ai_data will be False-y
        if not ai_data:
            print(f"⚠️ AI failed for {current_id}. Engaging rule-based fallback!")
            message_lower = customer_complaint.lower()
            
            # Default fallback values
            case_type = "other"
            severity = "medium"
            confidence = 0.5
            agent_summary = "Automated fallback triage applied due to AI system timeout."
            
            # Phishing Rules
            if any(word in message_lower for word in ["otp", "pin", "password", "scam"]):
                case_type = "phishing_or_social_engineering"
                severity = "critical"
            # Wrong Transfer Rules
            elif any(word in message_lower for word in ["wrong number", "mistake", "sent to wrong"]):
                case_type = "wrong_transfer"
                severity = "high"
            # Payment Failed Rules
            elif any(word in message_lower for word in ["failed", "didn't go through", "error"]):
                case_type = "payment_failed"
                
        else:
            # If the AI worked perfectly, extract its answers
            case_type = ai_data.get("case_type", "other")
            severity = ai_data.get("severity", "medium")
            agent_summary = ai_data.get("agent_summary", "Customer submitted a request.")
            confidence = ai_data.get("confidence", 1.0)
            
        # C. Deterministic Department Mapping
        department = DEPARTMENT_MAPPING.get(case_type, "customer_support")
        
        # D. The Human Review Rule
        human_review_required = False
        if severity == "critical" or case_type == "phishing_or_social_engineering":
            human_review_required = True
            
        # E. Package and return the final validated response
        return TicketResponse(
            ticket_id=current_id,
            case_type=case_type,
            severity=severity,
            department=department,
            agent_summary=agent_summary,
            human_review_required=human_review_required,
            confidence=float(confidence)
        )
        
    except Exception as e:
        # This only triggers if something goes horribly wrong with your own Python code
        print(f"Critical System Error on ticket {current_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
        

@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """
    Health check endpoint to verify that the service is running.
    """
    return {"status": "healthy"}