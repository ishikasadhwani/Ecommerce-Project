from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional, Union
from app.core.database import get_db
from app.utils.oauth2 import get_admin_user
from app.products import models, schemas
from app.orders.models import OrderItem
from app.products.schemas import MessageResponse, ProductOut
from fastapi import Query
from app.core.config import logger

router = APIRouter(prefix="/admin/products", tags=["Admin - Products"])
public_router = APIRouter(prefix="/products", tags=["Public - Products"])

# @router.post("/", status_code=status.HTTP_201_CREATED)
# def create_product(data: schemas.ProductCreate, db: Session = Depends(get_db), admin=Depends(get_admin_user)):
#     logger.info(f"Product creation requested by admin_id={admin.id} for product '{data.name}'")
#     product_data = data.dict()
#     product_data["image_url"] = str(product_data["image_url"]) if product_data["image_url"] else None
#     product_data["price"] = float(product_data["price"])  # Optional: if using Decimal
#     product = models.Product(**product_data)
#     db.add(product)
#     db.commit()
#     db.refresh(product)
#     logger.info(f"Product created successfully: id={product.id}, name={product.name}")
#     return {"message": "Product created successfully."}

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_product(
    data: schemas.ProductCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_admin_user)
):
    logger.info(f"Product creation requested by admin_id={admin.id} for product '{data.name}'")

    product_data = data.dict()
    product_data["image_url"] = str(product_data["image_url"]) if product_data["image_url"] else None
    product_data["price"] = float(product_data["price"])  # Optional: if using Decimal

    # ✅ Add creator relationship
    product = models.Product(**product_data, created_by=admin.id)

    db.add(product)
    db.commit()
    db.refresh(product)

    logger.info(f"Product created successfully: id={product.id}, name={product.name}")
    return {"message": "Product created successfully."}


@router.get("/", response_model=List[schemas.ProductOut])
def list_products(db: Session = Depends(get_db), admin=Depends(get_admin_user), skip: int = 0, limit: int = 10):
    logger.info(f"Product list requested by admin_id={admin.id}")
    return db.query(models.Product).offset(skip).limit(limit).all()

@router.get("/{product_id}", response_model=schemas.ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db), admin=Depends(get_admin_user)):
    logger.info(f"Product detail requested by admin_id={admin.id} for product_id={product_id}")
    product = db.query(models.Product).get(product_id)
    if not product:
        logger.warning(f"Product not found: product_id={product_id} requested by admin_id={admin.id}")
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/{product_id}", response_model=schemas.ProductUpdateResponse)
def update_product(
    product_id: int,
    data: schemas.ProductUpdate,
    db: Session = Depends(get_db),
    admin=Depends(get_admin_user)
):
    logger.info(f"Product update requested by admin_id={admin.id} for product_id={product_id}")
    
    product = db.query(models.Product).get(product_id)
    if not product:
        logger.warning(f"Product update failed: product_id={product_id} not found by admin_id={admin.id}")
        raise HTTPException(status_code=404, detail="Product not found")

    # ✅ Authorization check
    if product.created_by != admin.id:
        logger.warning(f"Unauthorized update attempt by admin_id={admin.id} on product_id={product_id}")
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to modify this product."
        )

    updates = data.dict(exclude_unset=True)

    if "image_url" in updates:
        updates["image_url"] = str(updates["image_url"]) if updates["image_url"] else None

    if "price" in updates:
        updates["price"] = float(updates["price"])

    for field, value in updates.items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)
    
    logger.info(f"Product updated successfully: product_id={product_id} by admin_id={admin.id}")
    return {
        "message": "Product updated successfully.",
        "product": product
    }


# @router.delete("/{product_id}")
# def delete_product(product_id: int, db: Session = Depends(get_db), admin=Depends(get_admin_user)):
#     logger.info(f"Product delete requested by admin_id={admin.id} for product_id={product_id}")
#     product = db.query(models.Product).get(product_id)
#     if not product:
#         logger.warning(f"Product delete failed: product_id={product_id} not found by admin_id={admin.id}")
#         raise HTTPException(status_code=404, detail="Product not found")
#     db.delete(product)
#     db.commit()
#     logger.info(f"Product deleted successfully: product_id={product_id} by admin_id={admin.id}")
#     return {"message": "Product deleted successfully"}

@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_admin_user)
):
    logger.info(f"Product delete requested by admin_id={admin.id} for product_id={product_id}")
    
    product = db.query(models.Product).get(product_id)
    if not product:
        logger.warning(f"Product delete failed: product_id={product_id} not found by admin_id={admin.id}")
        raise HTTPException(status_code=404, detail="Product not found")

    # ✅ Authorization check
    if product.created_by != admin.id:
        logger.warning(f"Unauthorized delete attempt by admin_id={admin.id} on product_id={product_id}")
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to delete this product."
        )

    db.delete(product)
    db.commit()
    
    logger.info(f"Product deleted successfully: product_id={product_id} by admin_id={admin.id}")
    return {"message": "Product deleted successfully"}



# @router.delete("/{product_id}")
# def delete_product(product_id: int, db: Session = Depends(get_db), admin=Depends(get_admin_user)):
#     logger.info(f"Product delete requested by admin_id={admin.id} for product_id={product_id}")
#     product = db.query(models.Product).get(product_id)
#     if not product:
#         logger.warning(f"Product delete failed: product_id={product_id} not found by admin_id={admin.id}")
#         raise HTTPException(status_code=404, detail="Product not found")

#     # Check for references in order_items
#     order_item = db.query(OrderItem).filter_by(product_id=product_id).first()
#     if order_item:
#         logger.warning(f"Product delete failed: product_id={product_id} is referenced in order_items")
#         raise HTTPException(status_code=400, detail="Cannot delete product: it is referenced in order items.")

#     db.delete(product)
#     db.commit()
#     logger.info(f"Product deleted successfully: product_id={product_id} by admin_id={admin.id}")
#     return {"message": "Product deleted successfully"}




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
    logger.info(f"Public product list requested with filters: category={category}, min_price={min_price}, max_price={max_price}, sort_by={sort_by}, page={page}, page_size={page_size}")
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
       logger.info("No products found matching the public query criteria.")
       return {
          "message": "No products found matching your criteria."
    }
    logger.info(f"Public product list returned {len(products)} products.")
    return products

@public_router.get("/search", response_model=Union[List[ProductOut], MessageResponse])
def search_products(keyword: str, db: Session = Depends(get_db)):
    logger.info(f"Public product search requested for keyword='{keyword}'")
    products = db.query(models.Product).filter(
        models.Product.name.ilike(f"%{keyword}%") |
        models.Product.description.ilike(f"%{keyword}%")
    ).all()

    if not products:
        logger.info(f"No products found for search keyword '{keyword}'.")
        return {"message": f"No products found for '{keyword}'."}
    
    logger.info(f"Search for '{keyword}' returned {len(products)} products.")
    return products

@public_router.get("/{id}", response_model=schemas.PublicProductOut)
def public_product_detail(id: int, db: Session = Depends(get_db)):
    logger.info(f"Public product detail requested for product_id={id}")
    product = db.query(models.Product).get(id)
    if not product:
        logger.warning(f"Public product detail failed: product_id={id} not found")
        raise HTTPException(status_code=404, detail="Product not found")
    logger.info(f"Public product detail returned for product_id={id}")
    return product
