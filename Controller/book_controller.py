from flask import Blueprint, request, jsonify

from Model.book_model import Book
from Service.book_service import BookService
from flask_restx import Namespace, Resource, fields

from Service.jwt_service import jwt_required
from database import db

book_bp = Blueprint('book', __name__, )

@book_bp.route('/', methods=['POST'])
@jwt_required
def add_book():
    try:
        data = request.get_json()
        if not data or not all(k in data for k in ['title', 'author']):
            return jsonify({"error": "Invalid data. 'title' and 'author' are required."}), 400

        new_book = BookService.add_book(data)
        if not isinstance(new_book, Book):  # Ensure the returned object is a Book instance
            return jsonify({"error": "Unexpected response from BookService"}), 500

        return jsonify(new_book.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@book_bp.route('/<int:book_id>', methods=['GET'])
@jwt_required
def get_book_by_id(book_id):
    try:
        book = BookService.get_book_by_id(book_id)
        if not book:
            return jsonify({"error": f"Book with ID {book_id} not found"}), 404

        return jsonify(book.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@book_bp.route('/<int:book_id>', methods=['PUT'])
@jwt_required
def update_book(book_id):
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400

        updated_book = BookService.update_book(book_id, data)
        if not updated_book:
            return jsonify({"error": f"Book with ID {book_id} not found"}), 404

        return jsonify(updated_book.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@book_bp.route('/<int:book_id>', methods=['DELETE'])
@jwt_required
def delete_book(book_id):
    try:
        book = BookService.delete_book(book_id)
        if not book:
            return jsonify({"error": f"Book with ID {book_id} not found"}), 404

        return jsonify({"message": f"Book with ID {book_id} deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Controller/book_controller.py
@book_bp.route('/', methods=['GET'])
@jwt_required
def get_books():
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=3, type=int)
    author = request.args.get('author', type=str)
    year = request.args.get('year', type=int)

    # Fetch books with filters and pagination
    pagination = BookService.get_filtered_books(page, per_page, author, year)
    books = pagination.items  # Get the items for the current page

    response = {
        "books": [book.to_dict() for book in books],
        "total": pagination.total,  # Total number of filtered books
        "pages": pagination.pages,  # Total number of pages
        "current_page": pagination.page  # Current page number
    }
    return jsonify(response), 200

book_ns = Namespace('books', description="Operations related to books")

# Define a book model for documentation
book_model = book_ns.model('Book', {
    'title': fields.String(required=True, description='The title of the book'),
    'author': fields.String(required=True, description='The author of the book'),
    'year': fields.Integer(required=False, description='The publication year of the book'),
    'isbn': fields.String(required=False, description='The ISBN of the book')
})

@book_ns.route('/books')
class BookList(Resource):

    @book_ns.doc('list_books')
    @book_ns.marshal_with(book_model, as_list=True)
    def get(self):
        """Get all books"""
        pagination = BookService.get_filtered_books(1, 3)
        books = pagination.items
        return books, 200

    @book_ns.expect(book_model)
    @book_ns.doc('create_book')
    # Protect the POST endpoint with JWT authentication
    def post(self):
        """Add a new book"""
        data = request.json
        new_book = Book(
            title=data['title'],
            author=data['author'],
            year=data['year'],
            isbn=data['isbn']
        )
        db.session.add(new_book)
        db.session.commit()
        return jsonify(new_book.to_dict()), 201


@book_ns.route('/<int:book_id>')
class BookDetail(Resource):
    @book_ns.doc('get_book_by_id')
    def get(self, book_id):
        """Get a book by its ID."""
        book = BookService.get_book_by_id(book_id)
        if not book:
            return {'message': 'Book not found'}, 404
        return book.to_dict(), 200

    @book_ns.expect(book_model)
    @book_ns.doc('update_book')
    @jwt_required # Protect the PUT endpoint with JWT authentication
    def put(self, book_id):
        """Update a book by ID."""
        data = request.json
        updated_book = BookService.update_book(book_id, data)
        if updated_book:
            return updated_book.to_dict(), 200
        return {'message': 'Book not found'}, 404

    @book_ns.doc('delete_book')
    @book_ns.response(204, 'Book deleted successfully')
    @jwt_required  # Protect the DELETE endpoint with JWT authentication
    def delete(self, book_id):
        """Delete a book by ID."""
        success = BookService.delete_book(book_id)
        if success:
            return '', 204
        return {'message': 'Book not found'}, 404
# Register the namespace with the main application
def register_book_namespace(api):
    api.add_namespace(book_ns)





