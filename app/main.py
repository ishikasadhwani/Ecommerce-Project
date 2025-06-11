from fastapi import FastAPI
from app.auth.models import User
from app.auth.routes import router as auth_router
from app.products.routes import router as product_router
from app.products.routes import public_router
from app.cart.routes import router as cart_router
from app.checkout.routes import router as checkout_router
from app.orders.routes import router as orders_router
from app.cart.models import CartItem
from app.core.database import Base, engine


app = FastAPI()


Base.metadata.create_all(bind=engine)
app.include_router(auth_router)
app.include_router(product_router)
app.include_router(public_router)
app.include_router(cart_router)
app.include_router(orders_router)
app.include_router(checkout_router)

@app.get("/")
def read_root():
    return {"message": "Hello World"}
