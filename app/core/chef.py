# app/core/chef.py
from app.schemas.order import CustomerOrder, RetentionResponse

def decide_retention_action(order: CustomerOrder) -> RetentionResponse:
    # High risk if churn > 0.7 OR sentiment is critical
    if order.churn_score > 0.7 or order.sentiment == "critical":
        discount = 20 if order.churn_score > 0.85 else 15
        clause = "RET-POL-4.2 (High-Risk Retention Credit)"
        email = (
            f"Hi {order.customer_id}, we are sorry about the issue in your ticket. "
            f"Per policy {clause}, we have applied a {discount}% discount to your account."
        )
        return RetentionResponse(
            customer_id=order.customer_id,
            status="DANGER",
            discount_offered_pct=discount,
            policy_clause_used=clause,
            draft_email=email
        )

    # Otherwise, customer is safe
    return RetentionResponse(
        customer_id=order.customer_id,
        status="SAFE",
        discount_offered_pct=0,
        policy_clause_used="NONE",
        draft_email="No retention discount needed. Route to standard support."
    )