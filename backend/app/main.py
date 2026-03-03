from fastapi import FastAPI
from app.database import engine, Base
from app.models import *
from app.routers import (
    customer_router,
    product_router,
    order_router,
    category_router,
    payment_router
)



app = FastAPI(
    title="E-Commerce API",
    version="1.0.0"
)
app.include_router(customer_router.router)
app.include_router(product_router.router)
app.include_router(order_router.router)
app.include_router(category_router.router)
app.include_router(payment_router.router)
@app.get("/")
def root():
    return {"message": "Backend is running 🚀"}
from sqlalchemy import text

@app.get("/test-db")
def test_db():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        return {"result": result.scalar()}
