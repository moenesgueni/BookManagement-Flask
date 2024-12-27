from database import db
from marshmallow import Schema, fields, validate
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
    class BookSchema(Schema):
        id = fields.Int(dump_only=True)
        title = fields.Str(required=True, validate=validate.Length(min=1, max=50))
        author = fields.Str(required=True, validate=validate.Length(min=1, max=50))
        year = fields.Int(required=True, validate=validate.Range(min=1800, max=2024))  # Validate publication year
        isbn = fields.Str(required=True, validate=validate.Regexp(r'^\d{13}$'))  # Validate ISBN

# Instantiate schema objects
    book_schema = BookSchema()
    books_schema = BookSchema(many=True)