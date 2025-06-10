from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional, Union
from app.core.database import get_db
from app.utils.oauth2 import get_admin_user
from app.products import models, schemas
from app.products.schemas import MessageResponse, ProductOut
from fastapi import Query

router = APIRouter(prefix="/admin/products", tags=["Admin - Products"])
public_router = APIRouter(prefix="/products", tags=["Public - Products"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_product(data: schemas.ProductCreate, db: Session = Depends(get_db), admin=Depends(get_admin_user)):
    product_data = data.dict()
    product_data["image_url"] = str(product_data["image_url"]) if product_data["image_url"] else None
    product_data["price"] = float(product_data["price"])  # Optional: if using Decimal
    product = models.Product(**product_data)
    db.add(product)
    db.commit()
    db.refresh(product)
    return {"message": "Product created successfully."}


@router.get("/", response_model=List[schemas.ProductOut])
def list_products(db: Session = Depends(get_db), admin=Depends(get_admin_user), skip: int = 0, limit: int = 10):
    return db.query(models.Product).offset(skip).limit(limit).all()

@router.get("/{product_id}", response_model=schemas.ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db), admin=Depends(get_admin_user)):
    product = db.query(models.Product).get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/{product_id}", response_model=schemas.ProductUpdateResponse)
def update_product(
    product_id: int,
    data: schemas.ProductUpdate,
    db: Session = Depends(get_db),
    admin=Depends(get_admin_user)
):
    product = db.query(models.Product).get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    updates = data.dict(exclude_unset=True)

    if "image_url" in updates:
        updates["image_url"] = str(updates["image_url"]) if updates["image_url"] else None

    if "price" in updates:
        updates["price"] = float(updates["price"])

    for field, value in updates.items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)
    return {
        "message": "Product updated successfully.",
        "product": product
    }

@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db), admin=Depends(get_admin_user)):
    product = db.query(models.Product).get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return {"message": "Product deleted successfully"}




@public_router.get("/", response_model=Union[List[ProductOut], MessageResponse])
def public_product_list(
    db: Session = Depends(get_db),
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    sort_by: Optional[str] = Query("price", enum=["price", "name", "stock"]),
    page: int = 1,
    page_size: int = 10
):
    query = db.query(models.Product)

    if category:
        query = query.filter(models.Product.category.ilike(f"%{category}%"))
    if min_price is not None:
        query = query.filter(models.Product.price >= min_price)
    if max_price is not None:
        query = query.filter(models.Product.price <= max_price)

    # Sorting
    if sort_by == "price":
        query = query.order_by(models.Product.price.asc())
    elif sort_by == "name":
        query = query.order_by(models.Product.name.asc())
    elif sort_by == "stock":
        query = query.order_by(models.Product.stock.desc())

    # Pagination
    products = query.offset((page - 1) * page_size).limit(page_size).all()
    if not products:
       return {
          "message": "No products found matching your criteria."
    }
    return products

@public_router.get("/search", response_model=Union[List[ProductOut], MessageResponse])
def search_products(keyword: str, db: Session = Depends(get_db)):
    products = db.query(models.Product).filter(
        models.Product.name.ilike(f"%{keyword}%") |
        models.Product.description.ilike(f"%{keyword}%")
    ).all()

    if not products:
        return {"message": f"No products found for '{keyword}'."}

    return products

@public_router.get("/{id}", response_model=schemas.PublicProductOut)
def public_product_detail(id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).get(id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
