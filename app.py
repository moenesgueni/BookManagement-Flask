from flask import Flask
from flask_restx import Api, Resource
from database import db

# Import your blueprints (controllers)
from Controller.book_controller import book_bp, register_book_namespace
from Controller.user_controller import user_bp

def create_app():
    app = Flask(__name__)

    # Configure the database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)

    # Register the Book namespace

    # Initialize Flask-RESTx API
    api = Api(app, title="Book Management API", version="1.0", description="API for managing books and users")
    register_book_namespace(api)
    # Register blueprints
    app.register_blueprint(book_bp, url_prefix='/books')
    app.register_blueprint(user_bp, url_prefix='/users')

    with app.app_context():
        db.create_all()  # Create tables if they don't exist

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
