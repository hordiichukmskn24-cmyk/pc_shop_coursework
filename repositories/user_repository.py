from database import db
from models.user import User

class UserRepository:
    @staticmethod
    def get_by_id(user_id: int):
        return User.query.get(user_id)

    @staticmethod
    def get_by_email(email: str):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def get_by_username(username: str):
        return User.query.filter_by(username=username).first()

    @staticmethod
    def add(user: User):
        db.session.add(user)
        db.session.commit()