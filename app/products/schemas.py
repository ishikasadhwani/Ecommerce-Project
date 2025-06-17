# Import necessary modules and classes
from pydantic import BaseModel, HttpUrl, condecimal, conint, Field
from typing import Optional
from decimal import Decimal

# Schemas for product operations in e-commerce application
class ProductCreate(BaseModel):
    name: str
    price: Decimal = Field(..., gt=0)  # type: Decimal
    # price: condecimal(gt=0)  # type: Decimal
    description: Optional[str] = None
    stock: int = Field(..., ge=0)  # type: int
    category: str
    image_url: Optional[HttpUrl]

class BasicProductOut(ProductCreate):
    id: int

    class Config:
        from_attributes = True

class ProductUpdate(ProductCreate):
    pass

class ProductOut(ProductCreate): 
    id: int
    created_by: int

    class Config:
        from_attributes = True

class ProductUpdateResponse(BaseModel):
    message: str
    product: ProductOut

class MessageResponse(BaseModel):
    message: str

class ProductOutOrders(BaseModel):
    name: str
    description: Optional[str]
    image_url: Optional[HttpUrl]

    class Config:
        from_attributes = True

class PublicProductOut(ProductOutOrders):
    price: float
    category: str

    class Config:
        from_attributes = True

