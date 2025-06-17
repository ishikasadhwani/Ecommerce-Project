from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Enum
from sqlalchemy.orm import relationship
from app.products.models import Product
from datetime import datetime
import enum
from app.core.database import Base

# Order status enum
class OrderStatus(str, enum.Enum):
    pending = "pending"
    paid = "paid"
    cancelled = "cancelled"

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    total_amount = Column(Float, nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.paid)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete")

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="SET NULL"),nullable=True)
    product_name = Column(String, nullable=False)  # snapshot
    product_description = Column(String, nullable=True)  # snapshot
    quantity = Column(Integer, nullable=False)
    price_at_purchase = Column(Float, nullable=False)
      
 
    order = relationship("Order", back_populates="items")
    product = relationship("Product")
