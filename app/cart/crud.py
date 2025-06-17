from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List
from app.cart import models
from app.products.models import Product


def add_to_cart(db: Session, user_id: int, product_id: int, quantity: int) -> str:
    """
    Adds a product to the user's cart. If already in cart, increase quantity.
    """
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found.")

    cart_item = db.query(models.CartItem).filter_by(user_id=user_id, product_id=product_id).first()

    if cart_item:
        cart_item.quantity += quantity
    else:
        db.add(models.CartItem(user_id=user_id, product_id=product_id, quantity=quantity))

    db.commit()
    return "Product added to cart."


def get_cart_items(db: Session, user_id: int) -> List[models.CartItem]:
    """
    Returns all cart items for a given user.
    """
    return db.query(models.CartItem).filter_by(user_id=user_id).all()


def update_cart_quantity(db: Session, user_id: int, product_id: int, quantity: int) -> str:
    """
    Updates the quantity of a specific product in the user's cart.
    """
    cart_item = db.query(models.CartItem).filter_by(user_id=user_id, product_id=product_id).first()

    if not cart_item:
        raise HTTPException(status_code=404, detail="Product not found in your cart.")

    cart_item.quantity = quantity
    db.commit()
    return "Cart item quantity updated successfully."


def remove_cart_item(db: Session, user_id: int, product_id: int) -> str:
    """
    Removes a product from the user's cart.
    """
    cart_item = db.query(models.CartItem).filter_by(user_id=user_id, product_id=product_id).first()

    if not cart_item:
        raise HTTPException(status_code=404, detail="Product not found in your cart.")

    db.delete(cart_item)
    db.commit()
    return "Product removed from cart successfully."
