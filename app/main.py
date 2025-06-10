from fastapi import FastAPI
from app.auth.models import User
from app.auth.routes import router as auth_router
from app.products.routes import router as product_router
from app.products.routes import public_router
from app.core.database import Base, engine


app = FastAPI()


Base.metadata.create_all(bind=engine)
app.include_router(auth_router)
app.include_router(product_router)
app.include_router(public_router)

@app.get("/")
def read_root():
    return {"message": "Hello World"}
