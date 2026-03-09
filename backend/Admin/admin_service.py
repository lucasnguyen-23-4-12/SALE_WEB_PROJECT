from sqlalchemy.orm import Session

from app.models.order import Order
from app.models.product import Product
from Admin.admin_schema import (
    OrderResponse,
    ProductCreate,
    ProductResponse,
    ProductUpdate,
)


def _read_stock(product: Product) -> int:
    if hasattr(product, "stock") and getattr(product, "stock") is not None:
        return int(getattr(product, "stock"))
    if hasattr(product, "units_in_stock") and getattr(product, "units_in_stock") is not None:
        return int(getattr(product, "units_in_stock"))
    return 0


def _write_stock(product: Product, stock: int) -> None:
    if hasattr(product, "stock"):
        setattr(product, "stock", stock)
    elif hasattr(product, "units_in_stock"):
        setattr(product, "units_in_stock", stock)


def _to_product_response(product: Product) -> ProductResponse:
    return ProductResponse(
        name=product.product_name,
        price=float(product.unit_price),
        stock=_read_stock(product),
        description=product.description,
    )


def _order_id_column():
    if hasattr(Order, "id"):
        return getattr(Order, "id")
    return Order.order_id


def _read_order_id(order: Order) -> int:
    if hasattr(order, "id") and getattr(order, "id") is not None:
        return int(getattr(order, "id"))
    return int(getattr(order, "order_id"))


def _read_user_id(order: Order) -> int:
    if hasattr(order, "user_id") and getattr(order, "user_id") is not None:
        return int(getattr(order, "user_id"))
    return int(getattr(order, "customer_id"))


def _read_total_price(order: Order) -> float:
    if hasattr(order, "total_price") and getattr(order, "total_price") is not None:
        return float(getattr(order, "total_price"))
    if hasattr(order, "total_amount") and getattr(order, "total_amount") is not None:
        return float(getattr(order, "total_amount"))

    order_items = getattr(order, "order_items", None)
    if order_items is not None:
        return float(
            sum(float(getattr(item, "amount", 0) or 0) for item in order_items)
        )

    return 0.0


def _read_created_at(order: Order):
    if hasattr(order, "created_at") and getattr(order, "created_at") is not None:
        return getattr(order, "created_at")
    if hasattr(order, "order_date") and getattr(order, "order_date") is not None:
        return getattr(order, "order_date")
    return None


def _to_order_response(order: Order) -> OrderResponse:
    return OrderResponse(
        id=_read_order_id(order),
        user_id=_read_user_id(order),
        total_price=_read_total_price(order),
        status=getattr(order, "status", "") or "",
        created_at=_read_created_at(order),
    )


def get_products(db: Session) -> list[ProductResponse]:
    products = db.query(Product).order_by(Product.product_id.asc()).all()
    return [_to_product_response(product) for product in products]


def get_orders(db: Session) -> list[OrderResponse]:
    orders = db.query(Order).order_by(_order_id_column().asc()).all()
    return [_to_order_response(order) for order in orders]


def get_order_by_id(db: Session, order_id: int) -> OrderResponse | None:
    order = db.query(Order).filter(_order_id_column() == order_id).first()
    if not order:
        return None
    return _to_order_response(order)


def update_order_status(
    db: Session,
    order_id: int,
    status: str,
) -> OrderResponse | None:
    order = db.query(Order).filter(_order_id_column() == order_id).first()
    if not order:
        return None

    order.status = status
    db.commit()
    db.refresh(order)
    return _to_order_response(order)


def create_product(db: Session, product: ProductCreate) -> ProductResponse:
    new_product = Product(
        product_name=product.name,
        unit_price=product.price,
        description=product.description,
    )
    _write_stock(new_product, product.stock)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return _to_product_response(new_product)


def update_product(
    db: Session,
    product_id: int,
    product: ProductUpdate
) -> ProductResponse | None:
    db_product = db.query(Product).filter(Product.product_id == product_id).first()
    if not db_product:
        return None

    if product.name is not None:
        db_product.product_name = product.name
    if product.price is not None:
        db_product.unit_price = product.price
    if product.description is not None:
        db_product.description = product.description
    if product.stock is not None:
        _write_stock(db_product, product.stock)

    db.commit()
    db.refresh(db_product)
    return _to_product_response(db_product)


def delete_product(db: Session, product_id: int) -> bool:
    db_product = db.query(Product).filter(Product.product_id == product_id).first()
    if not db_product:
        return False

    db.delete(db_product)
    db.commit()
    return True
