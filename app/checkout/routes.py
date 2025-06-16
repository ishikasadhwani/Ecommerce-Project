from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.auth.models import User
from app.utils.oauth2 import get_user_only
from app.products.models import Product
from app.cart.models import CartItem
from app.orders import models, schemas
from app.core.config import logger

router = APIRouter(
    tags=["Checkout"]
)

@router.post("/checkout", response_model=schemas.OrderResponseWithMessage, status_code=status.HTTP_201_CREATED)
def checkout(
    db: Session = Depends(get_db),
    user: User = Depends(get_user_only)
):
    logger.info(f"Checkout initiated by user_id={user.id}")
    """
    Checkout current user's cart and create a new order.
    - Validates stock
    - Deducts stock from inventory
    - Clears user's cart after order is placed
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
            logger.error(f"Checkout failed: Product not found (product_id={item.product_id}) for user_id={user.id}")
            raise HTTPException(status_code=404, detail=f"Product with ID {item.product_id} not found.")
        if product.stock < item.quantity:
            logger.warning(f"Checkout failed: Insufficient stock for product_id={product.id} (requested={item.quantity}, available={product.stock}) by user_id={user.id}")
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient stock for product '{product.name}'. Available: {product.stock}"
            )

        total_amount += product.price * item.quantity
        order_items.append({
            "product_id": product.id,
            "product_name": product.name,
            "product_description": product.description,
            "quantity": item.quantity,
            "price_at_purchase": product.price
        })

    # Create the Order
    order = models.Order(user_id=user.id, total_amount=total_amount)
    db.add(order)
    db.flush()  # To generate order.id before adding order items
    logger.info(f"Order created (order_id={order.id}) for user_id={user.id}")

    for item in order_items:
        db.add(models.OrderItem(order_id=order.id, **item))

        # Deduct stock
        product = db.query(Product).filter(Product.id == item["product_id"]).first()
        product.stock -= item["quantity"]

    # Clear cart
    db.query(CartItem).filter_by(user_id=user.id).delete()
    db.commit()
    db.refresh(order)

    logger.info(f"Checkout successful for user_id={user.id}, order_id={order.id}")

    return {
        "message": "Order placed successfully.",
        "order": order
    }
