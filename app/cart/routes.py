from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Union
from app.core.database import get_db
from app.utils.oauth2 import get_user_only
from app.cart import schemas, models
from app.products.models import Product
from app.cart.schemas import MessageResponse
from app.auth.models import User
from app.core.config import logger

router = APIRouter(prefix="/cart", tags=["Cart"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def add_to_cart(
    item: schemas.AddToCartSchema,
    db: Session = Depends(get_db),
    user: User = Depends(get_user_only)
):
    logger.info(f"Add to cart requested by user_id={user.id} for product_id={item.product_id} (qty={item.quantity})")
    """
    Add a product to the user's cart. If it already exists, update the quantity.
    """
    product = db.query(Product).filter(Product.id == item.product_id).first()
    if not product:
        logger.warning(f"Add to cart failed: Product not found (product_id={item.product_id}) by user_id={user.id}")
        raise HTTPException(status_code=404, detail="Product not found.")

    existing_item = db.query(models.CartItem).filter_by(user_id=user.id, product_id=item.product_id).first()
    if existing_item:
        existing_item.quantity += item.quantity
        logger.info(f"Updated quantity for product_id={item.product_id} in cart for user_id={user.id}")
    else:
        existing_item = models.CartItem(user_id=user.id, product_id=item.product_id, quantity=item.quantity)
        db.add(existing_item)
        logger.info(f"Added new product_id={item.product_id} to cart for user_id={user.id}")

    db.commit()
    return {"message": "Product added to cart."}

@router.get("/", response_model=Union[List[schemas.CartItemOut], MessageResponse])
def get_cart_items(
    db: Session = Depends(get_db),
    user: User = Depends(get_user_only)
):
    logger.info(f"Get cart items requested by user_id={user.id}")
    """
    Get all items in the current user's cart.
    """
    items= db.query(models.CartItem).filter_by(user_id=user.id).all()

    if not items:
        logger.info(f"Cart empty for user_id={user.id}")
        return {
          "message": "No items in the cart."
    }
    return items

@router.put("/{product_id}", status_code=status.HTTP_200_OK)
def update_cart_item_quantity(
    product_id: int,
    data: schemas.UpdateCartItemSchema,
    db: Session = Depends(get_db),
    user: User = Depends(get_user_only)
):
    """
    Update quantity of a product in the current user's cart.
    """
    logger.info(f"Update cart item quantity requested by user_id={user.id} for product_id={product_id} (qty={data.quantity})")
    cart_item = db.query(models.CartItem).filter_by(user_id=user.id, product_id=product_id).first()

    if not cart_item:
        logger.warning(f"Update cart item failed: Product not found in cart (product_id={product_id}) by user_id={user.id}")
        raise HTTPException(status_code=404, detail="Product not found in your cart.")

    cart_item.quantity = data.quantity
    db.commit()
    logger.info(f"Cart item quantity updated for product_id={product_id} by user_id={user.id}")
    return {"message": "Cart item quantity updated successfully."}

@router.delete("/{product_id}", status_code=status.HTTP_200_OK)
def remove_cart_item(
    product_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_user_only)
):
    """
    Remove a product from the current user's cart.
    """
    logger.info(f"Remove cart item requested by user_id={user.id} for product_id={product_id}")
    cart_item = db.query(models.CartItem).filter_by(user_id=user.id, product_id=product_id).first()

    if not cart_item:
        logger.warning(f"Remove cart item failed: Product not found in cart (product_id={product_id}) by user_id={user.id}")
        raise HTTPException(status_code=404, detail="Product not found in your cart.")

    db.delete(cart_item)
    db.commit()
    logger.info(f"Product removed from cart (product_id={product_id}) by user_id={user.id}")
    return {"message": "Product removed from cart successfully."}
