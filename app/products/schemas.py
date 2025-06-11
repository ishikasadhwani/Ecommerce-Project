from pydantic import BaseModel, HttpUrl, condecimal, conint
from typing import Optional

class ProductCreate(BaseModel):
    name: str
    description: Optional[str]
    price: condecimal(gt=0)
    stock: conint(ge=0)
    category: str
    image_url: Optional[HttpUrl]

class ProductUpdate(ProductCreate):
    pass

class ProductOut(ProductCreate):
    id: int

    class Config:
        orm_mode = True

class ProductUpdateResponse(BaseModel):
    message: str
    product: ProductOut

class MessageResponse(BaseModel):
    message: str

class PublicProductOut(BaseModel):
    name: str
    description: Optional[str]
    price: float
    category: str
    image_url: Optional[HttpUrl]

    class Config:
        orm_mode = True