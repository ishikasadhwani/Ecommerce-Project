# Import necessary modules
from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List
from app.cart import models
from app.products.models import Product
from app.core.config import logger


def add_to_cart(db: Session, user_id: int, product_id: int, quantity: int) -> str:
    """
    Adds a product to the user's cart.

    - If the product is out of stock, raise an error.
    - If the product is already in the cart, do not add again, ask to update quantity.
    """

    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        logger.warning(f"Add to cart failed: Product not found (product_id={product_id}) by user_id={user_id}")
        raise HTTPException(status_code=404, detail="Product not found.")

    if product.stock == 0:
        logger.warning(f"Add to cart failed: Product is out of stock (product_id={product_id}) for user_id={user_id}")
        raise HTTPException(status_code=400, detail="Product is out of stock.")

    existing_item = db.query(models.CartItem).filter_by(user_id=user_id, product_id=product_id).first()

    if existing_item:
        logger.warning(f"Add to cart blocked: Product already in cart (product_id={product_id}) for user_id={user_id}")
        raise HTTPException(
            status_code=409,
            detail="Product already in cart. Please update the quantity if needed."
        )

    # Add to cart
    new_cart_item = models.CartItem(
        user_id=user_id,
        product_id=product_id,
        quantity=quantity
    )
    db.add(new_cart_item)
    db.commit()
    
    logger.info(f"Product added to cart: product_id={product_id}, user_id={user_id}")

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
