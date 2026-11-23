# app/api/routes.py
from fastapi import APIRouter, status
from app.schemas.order import CustomerOrder, RetentionResponse
from app.core.chef import retention_service 

router = APIRouter()

@router.post(
    "/check-customer",
    response_model=RetentionResponse,
    status_code=status.HTTP_200_OK,
    summary="Asynchronous churn & retention evaluation endpoint"
)
async def check_customer(order: CustomerOrder) -> RetentionResponse:
    # Await the async service call so FastAPI can handle other requests concurrently
    return await retention_service.generate_retention_plan_async(payload=order)