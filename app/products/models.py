from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.core.database import Base
from sqlalchemy.orm import relationship

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    category = Column(String)
    image_url = Column(String)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    creator = relationship("User", back_populates="products")

    
