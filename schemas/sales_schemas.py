from datetime import datetime
from pydantic import BaseModel
from typing import List

class CreateSalesCheck(BaseModel):
    products: list[dict]
    payment_type: str
    payment_amount: float

class SalesCheckListResponse(BaseModel):
    total: int
    sales_checks: List[dict]

class SalesCheckResponse(BaseModel):
    id: int
    user_id: int
    created_at: datetime
    products: List[dict]
    payment: dict
    total: float
    rest: float