# app/api/routes.py
from fastapi import APIRouter
from app.schemas.order import CustomerOrder, RetentionResponse
from app.core.chef import decide_retention_action

router = APIRouter()

@router.post("/check-customer", response_model=RetentionResponse)
def check_customer(order: CustomerOrder) -> RetentionResponse:
    return decide_retention_action(order)