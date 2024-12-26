# Service/user_service.py
from Model.user_model import User
from werkzeug.security import check_password_hash
from Service.jwt_service import generate_jwt
from werkzeug.security import generate_password_hash
from database import  db


class UserService:
    @staticmethod
    def authenticate(username, password):
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            return generate_jwt({"user_id": user.id, "username": user.username})
        return None

    @staticmethod
    def create_user(username, password):
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        try:
            db.session.add(new_user)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            return False



