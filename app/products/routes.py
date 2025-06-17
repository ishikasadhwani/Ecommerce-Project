from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional, Union, Dict

from app.core.database import get_db
from app.utils.oauth2 import get_admin_user
from app.products import schemas, crud
from app.core.config import logger
from app.products.models import Product

router = APIRouter(prefix="/admin/products", tags=["Admin - Products"])
public_router = APIRouter(prefix="/products", tags=["Public - Products"])


# ------------------ ADMIN ROUTES ------------------

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Dict[str, str])
def create_product(
    data: schemas.ProductCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_admin_user)
) -> dict:
    """
    Admin-only: Create a new product.
    """
    product = crud.create_product(db, data, admin.id)
    logger.info(f"Product created successfully: id={product.id}, name={product.name}")
    return {"message": "Product created successfully."}


@router.get("/", response_model=List[schemas.ProductOut])
def list_products(
    db: Session = Depends(get_db),
    admin=Depends(get_admin_user),
    skip: int = 0,
    limit: int = 10
) -> List[schemas.ProductOut]:
    """
    Admin-only: Get paginated list of products.
    """
    logger.info(f"Product list requested by admin_id={admin.id}")
    return crud.list_products(db, skip, limit)


@router.get("/{product_id}", response_model=schemas.ProductOut)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_admin_user)
) -> schemas.ProductOut:
    """
    Admin-only: Get product by ID.
    """
    logger.info(f"Product detail requested by admin_id={admin.id} for product_id={product_id}")
    product = crud.get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.put("/{product_id}", response_model=schemas.ProductUpdateResponse)
def update_product(
    product_id: int,
    data: schemas.ProductUpdate,
    db: Session = Depends(get_db),
    admin=Depends(get_admin_user)
) -> Dict[str, Union[str, schemas.ProductOut]]:
    """
    Admin-only: Update product if created by the same admin.
    """
    logger.info(f"Update request for product_id={product_id} by admin_id={admin.id}")
    updated_product = crud.update_product(db, product_id, data.dict(exclude_unset=True), admin.id)
    return {
        "message": "Product updated successfully.",
        "product": updated_product
    }


@router.delete("/{product_id}", response_model=Dict[str, str])
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_admin_user)
) -> dict:
    """
    Admin-only: Delete product if created by the same admin.
    """
    logger.info(f"Delete request for product_id={product_id} by admin_id={admin.id}")
    crud.delete_product(db, product_id, admin.id)
    return {"message": "Product deleted successfully"}


# ------------------ PUBLIC ROUTES ------------------

@public_router.get("/", response_model=Union[List[schemas.BasicProductOut], schemas.MessageResponse])
def public_product_list(
    db: Session = Depends(get_db),
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    sort_by: Optional[str] = Query("price", enum=["price", "name", "stock"]),
    page: int = 1,
    page_size: int = 10
) -> Union[List[schemas.BasicProductOut], Dict[str, str]]:
    """
    Public: Filter and list products based on category, price range, and sorting.
    """
    logger.info("Public product list requested")
    products = crud.filter_public_products(db, category, min_price, max_price, sort_by, page, page_size)
    if not products:
        return {"message": "No products found matching your criteria."}
    return products


@public_router.get("/search", response_model=Union[List[schemas.BasicProductOut], schemas.MessageResponse])
def search_products(keyword: str, db: Session = Depends(get_db)) -> Union[List[schemas.BasicProductOut], Dict[str, str]]:
    """
    Public: Search products by name or description.
    """
    logger.info(f"Public search for keyword='{keyword}'")
    products = crud.search_products(db, keyword)
    if not products:
        return {"message": f"No products found for '{keyword}'."}
    return products


@public_router.get("/{id}", response_model=schemas.BasicProductOut)
def public_product_detail(id: int, db: Session = Depends(get_db)) -> schemas.BasicProductOut:
    """
    Public: Get product details by ID.
    """
    logger.info(f"Public product detail requested for id={id}")
    product = crud.get_product_by_id(db, id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

