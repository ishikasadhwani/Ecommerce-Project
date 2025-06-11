from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from typing import List
from app.core.database import get_db
from app.auth.models import User
from app.utils.oauth2 import get_user_only
from app.products.models import Product
from app.cart.models import CartItem
from app.orders import models, schemas

router = APIRouter(
    tags=["Orders"]
)

@router.post("/checkout", response_model=schemas.OrderResponseWithMessage, status_code=status.HTTP_201_CREATED)
def checkout(
    db: Session = Depends(get_db),
    user: User = Depends(get_user_only)
):
    """
    Checkout current user's cart and create a new order.
    - Validates stock
    - Deducts stock from inventory
    - Clears user's cart after order is placed
    """
    cart_items = db.query(CartItem).filter_by(user_id=user.id).all()

    if not cart_items:
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
                detail=f"Insufficient stock for product '{product.name}'. Available: {product.stock}"
            )

        total_amount += product.price * item.quantity
        order_items.append({
            "product_id": product.id,
            "quantity": item.quantity,
            "price_at_purchase": product.price
        })

    # Create the Order
    order = models.Order(user_id=user.id, total_amount=total_amount)
    db.add(order)
    db.flush()  # To generate order.id before adding order items

    for item in order_items:
        db.add(models.OrderItem(order_id=order.id, **item))

        # Deduct stock
        product = db.query(Product).filter(Product.id == item["product_id"]).first()
        product.stock -= item["quantity"]

    # Clear cart
    db.query(CartItem).filter_by(user_id=user.id).delete()
    db.commit()
    db.refresh(order)

    return {
        "message": "Order placed successfully.",
        "order": order
    }

@router.get("/orders", response_model=List[schemas.OrderOut])
def get_user_orders(
    db: Session = Depends(get_db),
    user: User = Depends(get_user_only)
):
    """
    Get a list of all orders placed by the current user.
    If no orders found, return a friendly message.
    """
    orders = db.query(models.Order).filter_by(user_id=user.id).order_by(models.Order.created_at.desc()).all()

    if not orders:
        return {"message": "No previous orders."}
    
    return orders

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
    order = db.query(models.Order).options(
        joinedload(models.Order.items).joinedload(models.OrderItem.product)
    ).filter_by(id=order_id, user_id=user.id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found.")

    return order