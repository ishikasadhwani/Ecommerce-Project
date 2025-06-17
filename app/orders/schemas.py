# Import necessary modules and classes
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
    product_name: str
    product_description: Optional[str] = None
    quantity: int
    price_at_purchase: float
    class Config:
        from_attributes = True

class OrderItemOutWithSubtotal(OrderItemOutHistory):
    """
    Response schema for a single item in an order with subtotal.
    """
    
    subtotal: Optional[float] = None

    class Config:
        from_attributes = True

class OrderItemOutCheckout(BaseModel):
    """
    Response schema for a single item in an order during checkout.
    """
    product: ProductOutOrders
    quantity: int
    price_at_purchase: float
    
    class Config:
        from_attributes = True

class OrderOutHistory(BaseModel):
    """
    Response schema for a complete order with nested items.
    """
    id: int
    total_amount: float
    status: OrderStatus
    created_at: datetime

    class Config:
        from_attributes = True

class OrderOutCheckout(OrderOutHistory):
    """
    Response schema for a complete order during checkout.
    """
    items: List[OrderItemOutCheckout]

    class Config:
        from_attributes = True


class OrderOut(BaseModel):
    """
    Response schema for a complete order with nested items.
    """
    id: int
    total_amount: float
    status: OrderStatus
    created_at: datetime
    items: List[OrderItemOutWithSubtotal]

    class Config:
        from_attributes = True

class OrderResponseWithMessage(BaseModel):
    message: str
    order: OrderOutCheckout

    class Config:
        from_attributes = True

class MessageResponse(BaseModel):
    message: str
