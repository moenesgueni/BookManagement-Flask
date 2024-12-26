from flask_sqlalchemy import SQLAlchemy

# Initialize the SQLAlchemy object
db = SQLAlchemy()

def init_db(app):
    """Bind the database to the Flask app and create tables."""
    db.init_app(app)
    with app.app_context():
        db.create_all()
