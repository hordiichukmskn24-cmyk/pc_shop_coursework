from database import db
from models.order import Order, OrderItem

class OrderRepository:
    @staticmethod
    def get_by_id(order_id: int):
        return Order.query.get(order_id)

    @staticmethod
    def get_by_user(user_id: int):
        return Order.query.filter_by(user_id=user_id).order_by(Order.created_at.desc()).all()

    @staticmethod
    def get_all():
        return Order.query.order_by(Order.created_at.desc()).all()

    @staticmethod
    def add(order: Order):
        db.session.add(order)
        db.session.commit()