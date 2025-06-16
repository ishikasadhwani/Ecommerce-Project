from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum
from app.products.schemas import ProductOutOrders

# Enum for order status
class OrderStatus(str, Enum):
    pending = "pending"
    paid = "paid"
    cancelled = "cancelled"

class OrderItemOutHistory(BaseModel):
    """
    Response schema for a single item in an order.
    """
    product: ProductOutOrders
    quantity: int
    price_at_purchase: float

    class Config:
        orm_mode = True

class OrderItemOutDetail(OrderItemOutHistory):
    """
    Response schema for a single item in an order.
    """
    
    subtotal: Optional[float] = None

    class Config:
        orm_mode = True

    
class OrderOutHistory(BaseModel):
    """
    Response schema for a complete order with nested items.
    """
    id: int
    total_amount: float
    status: OrderStatus
    created_at: datetime
    items: List[OrderItemOutHistory]

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
    items: List[OrderItemOutDetail]

    class Config:
        orm_mode = True

class OrderResponseWithMessage(BaseModel):
    message: str
    order: OrderOutHistory

    class Config:
        orm_mode = True

class MessageResponse(BaseModel):
    message: str
