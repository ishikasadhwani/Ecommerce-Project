# Import necessary modules and classes
from pydantic import BaseModel, conint
from typing import Optional, Annotated
from app.products.schemas import PublicProductOut

# Schemas for cart operations
class AddToCartSchema(BaseModel):
    product_id: int
    quantity: Annotated[int, conint(ge=1)]

class UpdateCartItemSchema(BaseModel):
    quantity: Annotated[int, conint(ge=1)]

class CartItemOut(BaseModel):
    id: int
    product: PublicProductOut
    quantity: int

    class Config:
        from_attributes = True

class MessageResponse(BaseModel):
    message: str