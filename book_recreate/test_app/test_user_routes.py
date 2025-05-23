import pytest
from fastapi.testclient import TestClient
from uuid import uuid4
from main import app
from database import users 

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_users():
    users.clear()


def test_create_user():
    user_data = {
        "name": "Alice",
        "email": "alice@example.com",
        "password": "secret"
    }
    response = client.post("/users", json=user_data)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["name"] == user_data["name"]
    assert json_data["email"] == user_data["email"]
    assert "id" in json_data


def test_list_users():
    client.post("/users", json={"name": "Alice", "email": "alice@example.com", "password": "secret"})
    client.post("/users", json={"name": "Bob", "email": "bob@example.com", "password": "pass123"})
    response = client.get("/users")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_single_user():
    post_response = client.post("/users", json={"name": "Charlie", "email": "charlie@example.com", "password": "pass"})
    user_id = post_response.json()["id"]
    get_response = client.get(f"/users/{user_id}")
    assert get_response.status_code == 200
    assert get_response.json()["email"] == "charlie@example.com"


def test_get_user_not_found():
    response = client.get(f"/users/{uuid4()}")
    assert response.status_code == 404


def test_update_user():
    post_response = client.post("/users", json={"name": "Dave", "email": "dave@example.com", "password": "pass"})
    user_id = post_response.json()["id"]
    update_data = {"name": "David"}
    put_response = client.put(f"/users/{user_id}", json=update_data)
    assert put_response.status_code == 200
    assert put_response.json()["name"] == "David"


def test_delete_user():
    post_response = client.post("/users", json={"name": "Eve", "email": "eve@example.com", "password": "pass"})
    user_id = post_response.json()["id"]
    del_response = client.delete(f"/users/{user_id}")
    assert del_response.status_code == 200
    assert del_response.json()["message"] == "User deleted successfully"

    # Verify deletion
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 404


def test_login_success():
    client.post("/users", json={"name": "Frank", "email": "frank@example.com", "password": "mypassword"})
    login_data = {"email": "frank@example.com", "password": "mypassword"}
    response = client.post("/users/login", json=login_data)
    assert response.status_code == 200
    assert "user_id" in response.json()


def test_login_failure():
    client.post("/users", json={"name": "Grace", "email": "grace@example.com", "password": "pass"})
    login_data = {"email": "grace@example.com", "password": "wrong"}
    response = client.post("/users/login", json=login_data)
    assert response.status_code == 401


def test_change_password_success():
    post_response = client.post("/users", json={"name": "Henry", "email": "henry@example.com", "password": "oldpass"})
    user_id = post_response.json()["id"]

    change_data = {"old_password": "oldpass", "new_password": "newpass"}
    response = client.post(f"/users/{user_id}/change-password", json=change_data)
    assert response.status_code == 200
    assert response.json()["message"] == "Password updated successfully"

    # Login with new password
    login_response = client.post("/users/login", json={"email": "henry@example.com", "password": "newpass"})
    assert login_response.status_code == 200


def test_change_password_fail_wrong_old():
    post_response = client.post("/users", json={"name": "Ivy", "email": "ivy@example.com", "password": "oldpass"})
    user_id = post_response.json()["id"]

    change_data = {"old_password": "wrongpass", "new_password": "newpass"}
    response = client.post(f"/users/{user_id}/change-password", json=change_data)
    assert response.status_code == 400
