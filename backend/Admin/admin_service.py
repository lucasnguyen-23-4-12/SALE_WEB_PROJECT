from sqlalchemy.orm import Session

from app.models.product import Product
from Admin.admin_schema import ProductCreate, ProductResponse, ProductUpdate


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


def get_products(db: Session) -> list[ProductResponse]:
    products = db.query(Product).order_by(Product.product_id.asc()).all()
    return [_to_product_response(product) for product in products]


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
