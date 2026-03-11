import logging

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import ValidationError
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


logger = logging.getLogger("app")


def _error_payload(
    *,
    code: str,
    message: str,
    details=None,
):
    payload = {"error": {"code": code, "message": message}}
    if details is not None:
        payload["error"]["details"] = details
    return payload


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            **_error_payload(code="http_error", message=str(exc.detail)),
        },
    )


@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "detail": exc.errors(),
            **_error_payload(code="validation_error", message="Request validation failed", details=exc.errors()),
        },
    )


@app.exception_handler(ValidationError)
async def pydantic_validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "detail": exc.errors(),
            **_error_payload(code="validation_error", message="Validation failed", details=exc.errors()),
        },
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled error: %s %s", request.method, request.url, exc_info=exc)
    return JSONResponse(
        status_code=500,
        content=_error_payload(code="internal_error", message="Internal server error"),
    )


@app.get("/")
def root():
    return {"message": "Backend is running 🚀"}


@app.get("/test-db")
def test_db():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        return {"result": result.scalar()}
