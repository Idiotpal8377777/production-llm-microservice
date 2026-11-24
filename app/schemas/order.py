# app/schemas/order.py
from typing import Literal
from pydantic import BaseModel, Field

# 1. INCOMING GUARD (Inspects what the customer sends in)
class CustomerOrder(BaseModel):
    customer_id: str = Field(..., min_length=4, description="Must be at least 4 characters")
    churn_score: float = Field(..., ge=0.0, le=1.0, description="Must be between 0.0 and 1.0")
    sentiment: Literal["low", "medium", "high", "critical"] = Field(..., description="Ticket urgency")
    ticket_text: str = Field(..., min_length=10, description="The customer's complaint")

# 2. OUTGOING GUARD (Inspects what our AI Chef sends back out!)
class RetentionResponse(BaseModel):
    customer_id: str = Field(..., min_length=4, description="Must be at least 4 characters")
    status: Literal["DANGER", "SAFE"]
    discount_offered_pct: int = Field(..., ge=0, le=20, description="Discount must be between 0 and 20 , Never exceed 20%")
    policy_clause_used: str
    draft_email: str