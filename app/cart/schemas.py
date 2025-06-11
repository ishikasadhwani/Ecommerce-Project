from pydantic import BaseModel, conint
from typing import Optional
from app.products.schemas import PublicProductOut

class AddToCartSchema(BaseModel):
    product_id: int
    quantity: conint(ge=1)

class UpdateCartItemSchema(BaseModel):
    quantity: conint(ge=1)

class CartItemOut(BaseModel):
    id: int
    product: PublicProductOut
    quantity: int

    class Config:
        orm_mode = True
