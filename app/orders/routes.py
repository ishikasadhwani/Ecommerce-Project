from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List, Union, Dict

from app.core.database import get_db
from app.auth.models import User
from app.utils.oauth2 import get_user_only
from app.orders import models, schemas, crud
from app.orders.schemas import MessageResponse
from app.core.config import logger

router = APIRouter(tags=["Orders"])


@router.get("/orders", response_model=Union[List[schemas.OrderOutHistory], MessageResponse])
def get_user_orders(
    db: Session = Depends(get_db),
    user: User = Depends(get_user_only)
) -> Union[List[schemas.OrderOutHistory], Dict[str, str]]:
    """
    Get all orders for the current user. Return message if none found.
    """
    logger.info(f"Order history requested by user_id={user.id}")
    orders = crud.get_user_orders(db, user.id)

    if not orders:
        logger.info(f"No previous orders found for user_id={user.id}")
        return {"message": "No previous orders."}
    
    logger.info(f"Found {len(orders)} orders for user_id={user.id}")
    return orders


@router.get("/orders/{order_id}", response_model=schemas.OrderOut)
def get_user_order_detail(
    order_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_user_only)
) -> schemas.OrderOut:
    """
    Get a specific order's detail, ensuring it belongs to the current user.
    """
    logger.info(f"Order detail requested for order_id={order_id} by user_id={user.id}")
    order = crud.get_order_detail_with_subtotals(db, order_id, user.id)
    logger.info(f"Order detail returned for order_id={order_id} by user_id={user.id}")
    return order
