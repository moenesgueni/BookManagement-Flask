from flask_sqlalchemy import SQLAlchemy

# Initialize the SQLAlchemy object
db = SQLAlchemy()

def init_db(app):
    """Bind the database to the Flask app and create tables."""
    db.init_app(app)
    with db.engine.connect() as conn:
        conn.execute("ALTER TABLE user ADD COLUMN role VARCHAR(20) NOT NULL DEFAULT 'user';")
    with app.app_context():
        db.create_all()
