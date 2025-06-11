from pydantic import BaseModel
from typing import List
from datetime import datetime
from enum import Enum

# Enum for order status
class OrderStatus(str, Enum):
    pending = "pending"
    paid = "paid"
    cancelled = "cancelled"

class OrderItemOut(BaseModel):
    """
    Response schema for a single item in an order.
    """
    product_id: int
    quantity: int
    price_at_purchase: float

    class Config:
        orm_mode = True

class OrderOut(BaseModel):
    """
    Response schema for a complete order with nested items.
    """
    id: int
    total_amount: float
    status: OrderStatus
    created_at: datetime
    items: List[OrderItemOut]

    class Config:
        orm_mode = True

class OrderResponseWithMessage(BaseModel):
    message: str
    order: OrderOut

    class Config:
        orm_mode = True

class OrderStatusUpdate(BaseModel):
    """
    Schema for updating an order's status.
    """
    status: OrderStatus
