from app import db
from app.models.book import Book
from flask import Blueprint, jsonify, make_response, request

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


@ books_bp.route("/<book_id>", methods=["GET", "PUT", "DELETE"])
def handle_book(book_id):

    book = Book.query.get(book_id)
    if book is None:
        return make_response("", 404)

    if request.method == "GET":
        return book.to_dict()
    elif request.method == "PUT":
        form_data = request.get_json()

        book.title = form_data["title"]
        book.description = form_data["description"]

        db.session.commit()

        return make_response(f"Book #{book.id} successfully updated")
    elif request.method == "DELETE":
        db.session.delete(book)
        db.session.commit()
        return make_response(f"Book #{book.id} successfully deleted")
