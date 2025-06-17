# Import necessary modules and dependencies
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Union, Dict

from app.cart import schemas, crud
from app.core.database import get_db
from app.utils.oauth2 import get_user_only
from app.auth.models import User
from app.cart.schemas import CartItemOut, MessageResponse
from app.core.config import logger

router = APIRouter(prefix="/cart", tags=["Cart"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Dict[str, str])
def add_to_cart(
    item: schemas.AddToCartSchema,
    db: Session = Depends(get_db),
    user: User = Depends(get_user_only)
) -> dict:
    """
    Add a product to the user's cart. If already exists, increase the quantity.
    """
    logger.info(f"User {user.id} adding product {item.product_id} (qty={item.quantity}) to cart.")
    message = crud.add_to_cart(db, user.id, item.product_id, item.quantity)
    return {"message": message}


@router.get("/", response_model=Union[List[CartItemOut], MessageResponse])
def get_cart_items(
    db: Session = Depends(get_db),
    user: User = Depends(get_user_only)
) -> Union[List[CartItemOut], Dict[str, str]]:
    """
    Retrieve all items in the current user's cart.
    """
    logger.info(f"Fetching cart items for user_id={user.id}")
    items = crud.get_cart_items(db, user.id)
    if not items:
        return {"message": "No items in the cart."}
    return items


@router.put("/{product_id}", status_code=status.HTTP_200_OK, response_model=Dict[str, str])
def update_cart_item_quantity(
    product_id: int,
    data: schemas.UpdateCartItemSchema,
    db: Session = Depends(get_db),
    user: User = Depends(get_user_only)
) -> dict:
    """
    Update quantity of a specific product in the user's cart.
    """
    logger.info(f"User {user.id} updating quantity of product {product_id} to {data.quantity}")
    message = crud.update_cart_quantity(db, user.id, product_id, data.quantity)
    return {"message": message}


@router.delete("/{product_id}", status_code=status.HTTP_200_OK, response_model=Dict[str, str])
def remove_cart_item(
    product_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_user_only)
) -> dict:
    """
    Remove a specific product from the user's cart.
    """
    logger.info(f"User {user.id} removing product {product_id} from cart.")
    message = crud.remove_cart_item(db, user.id, product_id)
    return {"message": message}
