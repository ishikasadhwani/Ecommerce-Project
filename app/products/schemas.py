from pydantic import BaseModel, HttpUrl, condecimal, conint, Field
from typing import Optional
from decimal import Decimal

class ProductCreate(BaseModel):
    name: str
    price: Decimal = Field(..., gt=0)  # type: Decimal
    # price: condecimal(gt=0)  # type: Decimal
    stock: int = Field(..., ge=0)  # type: int
    category: str
    image_url: Optional[HttpUrl]

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

