from flask.wrappers import Response


def test_get_all_books_with_no_records(client):
    response = client.get("/books")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == []


def test_get_one_book(client, two_saved_books):
    # Act
    response = client.get("/books/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
        "id": 1,
        "title": "Ocean Book",
        "description": "watr 4evr"
    }


def test_get_one_book_with_no_records_returns_404(client):
    response = client.get("/books/1")
    assert response.status_code == 404


def test_get_all_books_returns_all_books(client, two_saved_books):
    response = client.get("/books")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == [
        {
            "id": 1,
            "title": "Ocean Book",
            "description": "watr 4evr"
        },
        {
            "description": "i luv 2 climb rocks",
            "title": "Mountain Book",
            "id": 2
        }
    ]


def test_create_book_with_json_returns_201(client):
    response = client.post(
        "/books", json={"title": "Skyward", "description": "good"})
    assert response.status_code == 201
