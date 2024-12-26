from database import db

class User(db.Model):
    __table_name__ = 'users'  # Ensure correct table name
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)