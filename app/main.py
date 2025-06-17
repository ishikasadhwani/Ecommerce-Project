# Import necessary modules and packages
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError
from app.auth.models import User
from app.auth.routes import router as auth_router
from app.products.routes import router as product_router
from app.products.routes import public_router
from app.cart.routes import router as cart_router
from app.checkout.routes import router as checkout_router
from app.orders.routes import router as orders_router
from app.cart.models import CartItem
from app.core.database import Base, engine
from app.exceptions.handler import (
    custom_http_exception_handler,
    custom_validation_exception_handler,
    global_exception_handler,
    integrity_error_handler,
)

# Creating app instance
app = FastAPI()

Base.metadata.create_all(bind=engine)

# Include routers for different functionalities
app.include_router(auth_router)
app.include_router(product_router)
app.include_router(public_router)
app.include_router(cart_router)
app.include_router(orders_router)
app.include_router(checkout_router)

# Custom exception handlers
app.add_exception_handler(RequestValidationError, handler=custom_validation_exception_handler)
app.add_exception_handler(HTTPException, handler=custom_http_exception_handler)
app.add_exception_handler(Exception, handler= global_exception_handler)
app.add_exception_handler(IntegrityError, handler= integrity_error_handler)

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the E-commerce Backend System!"}
