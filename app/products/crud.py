from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional
from app.products import models, schemas
from app.core.config import logger


def create_product(db: Session, data: schemas.ProductCreate, admin_id: int) -> models.Product:
    """
    Create a new product associated with the admin.
    """
    logger.info(f"Creating product '{data.name}' by admin_id={admin_id}")
    product_data = data.dict()
    product_data["image_url"] = str(product_data.get("image_url")) or None
    product_data["price"] = float(product_data["price"])

    product = models.Product(**product_data, created_by=admin_id)
    try:
        db.add(product)
        db.commit()
        db.refresh(product)
        return product
    
    except IntegrityError:
        db.rollback()
        logger.error(f"Conflict: Product with name '{data.name}' already exists.")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Product with name '{data.name}' already exists."
        )


def get_product_by_id(db: Session, product_id: int) -> Optional[models.Product]:
    """
    Fetch product by its ID.
    """
    return db.query(models.Product).get(product_id)


def list_products(db: Session, skip: int = 0, limit: int = 10) -> List[models.Product]:
    """
    List all products with pagination.
    """
    return db.query(models.Product).offset(skip).limit(limit).all()


def update_product(db: Session, product_id: int, updates: dict, admin_id: int) -> models.Product:
    """
    Update product fields, only if the admin is the creator.
    """
    product = get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.created_by != admin_id:
        raise HTTPException(status_code=403, detail="You are not authorized to modify this product.")

    if "image_url" in updates:
        updates["image_url"] = str(updates["image_url"]) or None
    if "price" in updates:
        updates["price"] = float(updates["price"])

    for key, value in updates.items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)
    return product


def delete_product(db: Session, product_id: int, admin_id: int) -> bool:
    """
    Delete product only if the admin created it.
    """
    product = get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.created_by != admin_id:
        raise HTTPException(status_code=403, detail="You are not authorized to delete this product.")

    db.delete(product)
    db.commit()
    return True


def filter_public_products(
    db: Session,
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    sort_by: str = "price",
    page: int = 1,
    page_size: int = 10
) -> List[models.Product]:
    """
    Filter public products based on various criteria.
    """
    query = db.query(models.Product)

    if category:
        query = query.filter(models.Product.category.ilike(f"%{category}%"))
    if min_price is not None:
        query = query.filter(models.Product.price >= min_price)
    if max_price is not None:
        query = query.filter(models.Product.price <= max_price)

    if sort_by == "price":
        query = query.order_by(models.Product.price.asc())
    elif sort_by == "name":
        query = query.order_by(models.Product.name.asc())
    elif sort_by == "stock":
        query = query.order_by(models.Product.stock.desc())

    return query.offset((page - 1) * page_size).limit(page_size).all()


def search_products(db: Session, keyword: str) -> List[models.Product]:
    """
    Search public products by keyword in name or description.
    """
    return db.query(models.Product).filter(
        models.Product.name.ilike(f"%{keyword}%") |
        models.Product.description.ilike(f"%{keyword}%")
    ).all()
