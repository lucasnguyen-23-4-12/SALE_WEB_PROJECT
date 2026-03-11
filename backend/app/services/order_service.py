from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.product import Product
from app.models.customer import Customer
from app.models.payment_method import PaymentMethod
from app.services.exceptions import *
from datetime import datetime


def get_order_by_id(db: Session, order_id: str):
    """Lấy order theo ID"""
    order = db.query(Order).filter(
        Order.order_id == order_id
    ).first()

    if not order:
        raise NotFoundException("Order")

    return order


def get_all_orders(db: Session, skip: int = 0, limit: int = 10):
    """Lấy tất cả orders (có pagination)"""
    return db.query(Order).offset(skip).limit(limit).all()


def get_orders_by_customer(db: Session, customer_id: str, skip: int = 0, limit: int = 10):
    """Lấy orders theo customer (có pagination)"""
    return (
        db.query(Order)
        .filter(Order.customer_id == customer_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_order(db: Session, payload):
    """Tạo order mới - payload là OrderCreate schema"""
    customer_id = payload.customer_id
    payment_method_id = payload.payment_method_id
    shipping_address = getattr(payload, 'shipping_address', None)
    shipping_fee = getattr(payload, 'shipping_fee', 0.0)
    discount_amount = getattr(payload, 'discount_amount', 0.0)
    items = [item.model_dump() for item in payload.items]

    customer = db.query(Customer).filter(
        Customer.customer_id == customer_id
    ).first()

    if not customer:
        raise NotFoundException("Customer")

    payment_method = db.query(PaymentMethod).filter(
        PaymentMethod.payment_method_id == payment_method_id
    ).first()

    if not payment_method:
        raise NotFoundException("Payment Method")

    if not items:
        raise BusinessLogicException("Order must contain at least one item")

    try:
        new_order = Order(
            customer_id=customer_id,
            payment_method_id=payment_method_id,
            order_date=datetime.utcnow(),
            status="Pending",
            shipping_address=shipping_address,
            shipping_fee=shipping_fee,
            discount_amount=discount_amount
        )

        db.add(new_order)
        db.flush()

        total_amount = 0

        for item in items:

            if item["quantity"] <= 0:
                raise BusinessLogicException("Quantity must be greater than 0")

            product = db.query(Product).filter(
                Product.product_id == item["product_id"]
            ).first()

            if not product:
                raise NotFoundException(f"Product {item['product_id']}")

            price = product.unit_price
            amount = price * item["quantity"]

            total_amount += amount

            order_item = OrderItem(
                order_id=new_order.order_id,
                product_id=product.product_id,
                quantity=item["quantity"],
                amount=amount,
                price_at_purchase=price,
                profit=0,
                discount=0
            )

            db.add(order_item)

        db.commit()
        db.refresh(new_order)

        return new_order

    except SQLAlchemyError as e:
        db.rollback()
        raise BusinessLogicException("Database transaction failed")


def delete_order(db: Session, order_id: str):
    """Xóa order"""
    order = get_order_by_id(db, order_id)

    db.delete(order)
    db.commit()

    return {"message": "Order deleted successfully"}
