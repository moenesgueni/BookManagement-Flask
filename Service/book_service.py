from Model.book_model import Book
from database import db

class BookService:
    @staticmethod
    def get_all_books():
        return Book.query.all()


    @staticmethod
    def add_book(data):
        new_book = Book(
            title=data.get('title'),
            author=data.get('author'),
            year=data.get('year'),
            isbn=data.get('isbn')
        )
        db.session.add(new_book)
        db.session.commit()
        return new_book

    @staticmethod
    def get_book_by_id(book_id):
        return Book.query.get(book_id)

    @staticmethod
    def update_book(book_id, data):
        book = Book.query.get(book_id)
        if not book:
            return None

        # Update fields
        book.title = data.get('title', book.title)
        book.author = data.get('author', book.author)
        book.year = data.get('year', book.year)
        book.isbn = data.get('isbn', book.isbn)

        db.session.commit()
        return book

    @staticmethod
    def delete_book(book_id):
        book = Book.query.get(book_id)
        if not book:
            return None

        db.session.delete(book)
        db.session.commit()
        return book
