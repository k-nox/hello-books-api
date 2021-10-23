from app import db
from app.models.book import Book
from flask import Blueprint, jsonify, make_response, request

books_bp = Blueprint("books", __name__, url_prefix="/books")


@books_bp.route("", methods=["GET", "POST"])
def handle_books():
    if request.method == "GET":
        books = Book.query.all()
        books_response = [{"id": book.id, "title": book.title,
                           "description": book.description} for book in books]
        return jsonify(books_response)
    elif request.method == "POST":
        request_body = request.get_json()
        new_book = Book(title=request_body["title"],
                        description=request_body["description"])

        db.session.add(new_book)
        db.session.commit()

        return make_response(f"Book {new_book.title} successfully created", 201)


@books_bp.route("/<book_id>", methods=["GET", "PUT"])
def handle_book(book_id):

    book = Book.query.get(book_id)

    if request.method == "GET":
        return book.to_dict()
    elif request.method == "PUT":
        form_data = request.get_json()

        book.title = form_data["title"]
        book.description = form_data["description"]

        db.session.commit()

        return make_response(f"Book #{book.id} successfully updated")
