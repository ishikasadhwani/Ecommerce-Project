# Import necessary modules and classes
from sqlalchemy import Column, Integer, String, Boolean, Enum, ForeignKey, DateTime
from app.core.database import Base
import enum
from sqlalchemy.orm import relationship
from app.cart.models import CartItem
from app.orders.models import Order
from app.products.models import Product
 
# RoleEnum for user roles
class RoleEnum(str, enum.Enum):
    admin = "admin"
    user = "user"

# User model that represents the users of the e-commerce system
class User(Base):
    __tablename__ = "users"
    
    # Column definitions
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(RoleEnum), default=RoleEnum.user)
    
    # Relationships
    products = relationship("Product", back_populates="creator", cascade="all, delete")
    cart_items = relationship("CartItem", back_populates="user", cascade="all, delete")
    orders = relationship("Order", back_populates="user", cascade="all, delete")
   

# PasswordResetToken model for handling password reset tokens
class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"
    
    # Column definitions
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    used=Column(Boolean, default=False)
    
    # Relationships
    user = relationship("User")
