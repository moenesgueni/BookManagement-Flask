from flask import Flask

from Service.user_service import UserService
from database import db
from flask_sqlalchemy import SQLAlchemy
from Controller.book_controller import book_bp
from Controller.user_controller import user_bp

# Initialize the database


def create_app():
    app = Flask(__name__)

    # Configure the database (SQLite in this case)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'  # Path to your SQLite file
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)

    # Register blueprints
    app.register_blueprint(book_bp)
    app.register_blueprint(user_bp)

    with app.app_context():
        db.create_all()  # Ensure tables are created


    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
