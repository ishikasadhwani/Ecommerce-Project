from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException
from typing import List, Dict, Union

from app.orders import models


def get_user_orders(db: Session, user_id: int) -> List[models.Order]:
    """
    Retrieve all orders placed by a specific user, most recent first.
    """
    return db.query(models.Order)\
             .filter_by(user_id=user_id)\
             .order_by(models.Order.created_at.desc())\
             .all()


def get_order_detail_with_subtotals(db: Session, order_id: int, user_id: int) -> models.Order:
    """
    Retrieve order detail by ID with joined items and calculated subtotal.
    Ensures the order belongs to the current user.
    """
    order = db.query(models.Order)\
              .options(joinedload(models.Order.items))\
              .filter_by(id=order_id, user_id=user_id)\
              .first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found.")

    # Attach subtotal per item
    for item in order.items:
        item.subtotal = round(item.quantity * item.price_at_purchase, 2)

    return order
