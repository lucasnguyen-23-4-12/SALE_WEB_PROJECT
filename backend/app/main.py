from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.database import engine, Base
from app.models import *
from app.routers import (
    customer_router,
    product_router,
    order_router,
    category_router,
    payment_router,
    review_router,
    address_router,
    wishlist_router
)
from Admin import admin_router



app = FastAPI(
    title="E-Commerce API",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    # allow dev origins (IPv4, IPv6, localhost)
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://[::]:5500",
        "http://localhost:5500",
        "http://127.0.0.1:8000",
        "http://localhost:8000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(customer_router.router)
app.include_router(product_router.router)
app.include_router(order_router.router)
app.include_router(category_router.router)
app.include_router(payment_router.router)
app.include_router(review_router.router)
app.include_router(address_router.router)
app.include_router(wishlist_router.router)
app.include_router(admin_router.router)


@app.get("/")
def root():
    return {"message": "Backend is running 🚀"}


@app.get("/test-db")
def test_db():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        return {"result": result.scalar()}
