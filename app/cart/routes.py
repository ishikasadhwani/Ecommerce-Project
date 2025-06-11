from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Union
from app.core.database import get_db
from app.utils.oauth2 import get_user_only
from app.cart import schemas, models
from app.products.models import Product
from app.cart.schemas import MessageResponse
from app.auth.models import User

router = APIRouter(prefix="/cart", tags=["Cart"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def add_to_cart(
    item: schemas.AddToCartSchema,
    db: Session = Depends(get_db),
    user: User = Depends(get_user_only)
):
    """
    Add a product to the user's cart. If it already exists, update the quantity.
    """
    product = db.query(Product).filter(Product.id == item.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found.")

    existing_item = db.query(models.CartItem).filter_by(user_id=user.id, product_id=item.product_id).first()
    if existing_item:
        existing_item.quantity += item.quantity
    else:
        existing_item = models.CartItem(user_id=user.id, product_id=item.product_id, quantity=item.quantity)
        db.add(existing_item)

    db.commit()
    return {"message": "Product added to cart."}

@router.get("/", response_model=Union[List[schemas.CartItemOut], MessageResponse])
def get_cart_items(
    db: Session = Depends(get_db),
    user: User = Depends(get_user_only)
):
    """
    Get all items in the current user's cart.
    """
    items= db.query(models.CartItem).filter_by(user_id=user.id).all()

    if not items:
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
    cart_item = db.query(models.CartItem).filter_by(user_id=user.id, product_id=product_id).first()

    if not cart_item:
        raise HTTPException(status_code=404, detail="Product not found in your cart.")

    cart_item.quantity = data.quantity
    db.commit()
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
    cart_item = db.query(models.CartItem).filter_by(user_id=user.id, product_id=product_id).first()

    if not cart_item:
        raise HTTPException(status_code=404, detail="Product not found in your cart.")

    db.delete(cart_item)
    db.commit()
    return {"message": "Product removed from cart successfully."}
