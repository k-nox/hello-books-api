from app import db
from app.models.book import Book
from flask import Blueprint, jsonify, make_response, request, abort

books_bp = Blueprint("books", __name__, url_prefix="/books")


@books_bp.route("", methods=["GET"])
def read_books():
    title_query = request.args.get("title")
    if title_query:
        books = Book.query.filter_by(title=title_query)
    else:
        books = Book.query.all()
    return jsonify([book.to_dict() for book in books])


@books_bp.route("", methods=["POST"])
def create_book():
    request_body = request.get_json()
    try:
        new_book = Book(
            title=request_body["title"], description=request_body["description"])
        db.session.add(new_book)
        db.session.commit()
        return make_response(f"Book {new_book.title} successfully created", 201)
    except:
        return make_response("invalid book data to create book", 400)


def get_book_by_id(book_id):
    try:
        book_id = int(book_id)
    except:
        abort(400, "invalid id")
    return Book.query.get_or_404(book_id)


@books_bp.route("/<book_id>", methods=["GET"])
def read_book(book_id):
    book = get_book_by_id(book_id)
    return jsonify(book.to_dict())


@books_bp.route("/<book_id>", methods=["PATCH"])
def update_book(book_id):
    book = get_book_by_id(book_id)
    request_body = request.get_json()
    if "title" in request_body:
        book.title = request_body["title"]
    if "description" in request_body:
        book.description = request_body["description"]
    db.session.commit()

    return make_response(f"Book #{book.id} successfully updated", 200)


@books_bp.route("/<book_id>", methods=["DELETE"])
def delete_book(book_id):
    book = get_book_by_id(book_id)
    db.session.delete(book)
    db.session.commit()
    return make_response(f"Book #{book.id} successfully deleted", 200)
