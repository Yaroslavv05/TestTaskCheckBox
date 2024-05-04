from datetime import datetime
from pydantic import BaseModel
from typing import List

'''
Defines Pydantic models for data validation and serialization.

CreateSalesCheck: Pydantic model for validating data required to create a sales check, including products, payment type, and payment amount.

SalesCheckListResponse: Pydantic model for serializing a list of sales checks, including total count and details of each sales check.

SalesCheckResponse: Pydantic model for serializing details of a single sales check, including its ID, user ID, creation timestamp, 
products, payment details, total amount, and remaining amount.

'''

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