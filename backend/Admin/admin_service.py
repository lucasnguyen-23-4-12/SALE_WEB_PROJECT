from sqlalchemy.orm import Session

from app.models.order import Order
from app.schemas.order import OrderResponse, OrderUpdate
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate
from app.services import order_service, product_service


def get_products(db: Session, skip: int = 0, limit: int = 10) -> list[ProductResponse]:
    return product_service.get_all_products(db, skip=skip, limit=limit)


def get_product_by_id(db: Session, product_id: str) -> ProductResponse:
    return product_service.get_product_by_id(db, product_id)


def create_product(db: Session, payload: ProductCreate) -> ProductResponse:
    return product_service.create_product(db, payload)


def update_product(db: Session, product_id: str, payload: ProductUpdate) -> ProductResponse:
    return product_service.update_product(db, product_id, payload)


def delete_product(db: Session, product_id: str) -> None:
    product_service.delete_product(db, product_id)


def get_orders(db: Session, skip: int = 0, limit: int = 10) -> list[OrderResponse]:
    return order_service.get_all_orders(db, skip=skip, limit=limit)


def get_order_by_id(db: Session, order_id: str) -> OrderResponse:
    return order_service.get_order_by_id(db, order_id)


def update_order_status(db: Session, order_id: str, payload: OrderUpdate) -> Order:
    order = order_service.get_order_by_id(db, order_id)
    if payload.status is not None:
        order.status = payload.status
        db.commit()
        db.refresh(order)
    return order
