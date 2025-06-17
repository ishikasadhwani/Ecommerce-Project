# Import necessary modules
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import Dict

from app.auth.models import User
from app.products.models import Product
from app.cart.models import CartItem
from app.orders import models
from app.core.config import logger


def process_checkout(db: Session, user: User) -> Dict:
    """
    Handles full checkout process:
    - Verifies cart
    - Validates stock
    - Creates order and order items
    - Deducts inventory
    - Clears cart after success
    """
    cart_items = db.query(CartItem).filter_by(user_id=user.id).all()

    if not cart_items:
        logger.warning(f"Checkout failed: Cart empty for user_id={user.id}")
        raise HTTPException(status_code=400, detail="Your cart is empty.")

    total_amount = 0
    order_items = []

    for item in cart_items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product with ID {item.product_id} not found.")

        if product.stock < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient stock for '{product.name}'. Available: {product.stock}"
            )

        total_amount += product.price * item.quantity
        order_items.append({
            "product_id": product.id,
            "product_name": product.name,
            "product_description": product.description,
            "quantity": item.quantity,
            "price_at_purchase": product.price
        })

    # Create order
    order = models.Order(user_id=user.id, total_amount=total_amount)
    db.add(order)
    db.flush()  # generate order.id

    # Create order items and deduct stock
    for item in order_items:
        db.add(models.OrderItem(order_id=order.id, **item))
        product = db.query(Product).filter(Product.id == item["product_id"]).first()
        product.stock -= item["quantity"]

    # Clear the cart
    db.query(CartItem).filter_by(user_id=user.id).delete()
    db.commit()
    db.refresh(order)

    logger.info(f"Checkout successful for user_id={user.id}, order_id={order.id}")

    return {
        "message": "Order placed successfully.",
        "order": order
    }
