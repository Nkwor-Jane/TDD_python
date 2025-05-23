from fastapi.testclient import TestClient
from main import app
from schemas.book import BookCreate

client = TestClient(app)


def test_get_books():
    response = client.get("/books")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_add_book():
    payload = {
        "title": "Johny bravo",
        "author": "John Doe",
        "year": 2023,
        "pages": 500,
        "language": "English"
    }
    response = client.post("/books", json=payload)
    data = response.json()
    assert data["message"] == "Book added successfully"
    assert data["data"]["title"] == "Johny bravo"


def test_get_book_by_id():
    payload = {
        "title": "Johny bravo",
        "author": "John Doe",
        "year": 2023,
        "pages": 500,
        "language": "English"
    }
    response = client.post("/books", json=payload)
    add_book_data = response.json()
    book_id = add_book_data['data']['id']
    get_response = client.get(f"/books/{book_id}")
    get_book_data = get_response.json()
    assert get_response.status_code == 200
    assert get_book_data['id'] == book_id


def test_get_book_by_id_not_found():
    book_id = 1
    get_response = client.get(f"/books/{book_id}")
    get_book_data = get_response.json()
    assert get_response.status_code == 404
    assert get_book_data['detail'] == "book not found."
