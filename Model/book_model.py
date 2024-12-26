from database import db

class Book(db.Model):
    __table_name__ = 'books'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    title = db.Column(db.String(50), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=True)
    isbn = db.Column(db.String(50), nullable=True)

    def to_dict(self):
        return {
        "id": self.id,
        "title": self.title,
        "author": self.author,
        "year": self.year,
        "isbn": self.isbn
        }