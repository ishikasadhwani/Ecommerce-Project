from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from typing import List, Union
from app.core.database import get_db
from app.auth.models import User
from app.utils.oauth2 import get_user_only
from app.products.models import Product
from app.cart.models import CartItem
from app.orders import models, schemas
from app.orders.schemas import MessageResponse
from app.core.config import logger 

router = APIRouter(
    tags=["Orders"]
)

@router.get("/orders", response_model=Union[List[schemas.OrderOutHistory], MessageResponse])
def get_user_orders(
    db: Session = Depends(get_db),
    user: User = Depends(get_user_only)
):
    logger.info(f"Order history requested by user_id={user.id}")
    """
    Get a list of all orders placed by the current user.
    If no orders found, return a friendly message.
    """
    orders = db.query(models.Order).filter_by(user_id=user.id).order_by(models.Order.created_at.desc()).all()

    if not orders:
        logger.info(f"No previous orders found for user_id={user.id}")
        return {"message": "No previous orders."}
    
    logger.info(f"Found {len(orders)} orders for user_id={user.id}")
    return orders

def attach_subtotals(order):
    for item in order.items:
        item.subtotal = round(item.quantity * item.price_at_purchase, 2)
    return order

@router.get("/orders/{order_id}", response_model=schemas.OrderOut)
def get_user_order_detail(
    order_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_user_only)
):
    """
    Get detailed information about a specific order by order ID.
    Ensures the order belongs to the current user.
    """
    logger.info(f"Order detail requested for order_id={order_id} by user_id={user.id}")
    order = db.query(models.Order).options(
        joinedload(models.Order.items).joinedload(models.OrderItem.product)
    ).filter_by(id=order_id, user_id=user.id).first()
    if not order:
        logger.warning(f"Order not found: order_id={order_id} for user_id={user.id}")
        raise HTTPException(status_code=404, detail="Order not found.")
    
    logger.info(f"Order detail returned for order_id={order_id} by user_id={user.id}")
    return attach_subtotals(order)