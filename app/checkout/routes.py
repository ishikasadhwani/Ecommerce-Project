from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.auth.models import User
from app.utils.oauth2 import get_user_only
from app.orders import schemas
from app.checkout import crud
from typing import Dict, Union

router = APIRouter(tags=["Checkout"])


@router.post("/checkout", response_model=schemas.OrderResponseWithMessage, status_code=status.HTTP_201_CREATED)
def checkout(
    db: Session = Depends(get_db),
    user: User = Depends(get_user_only)
) -> Dict[str, Union[str, schemas.OrderOut]]:
    """
    User-only: Checkout the current cart, validate stock, create order, deduct inventory, and clear cart.
    """
    return crud.process_checkout(db, user)
