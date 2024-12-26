import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///instance/app.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
