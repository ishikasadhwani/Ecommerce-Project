# Import necessary modules and classes
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.core.database import Base
from sqlalchemy.orm import relationship

# Product model that represents the products in the e-commerce system
class Product(Base):
    __tablename__ = "products"
    
    # Column definitions
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    category = Column(String)
    image_url = Column(String)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationships
    creator = relationship("User", back_populates="products")

    
