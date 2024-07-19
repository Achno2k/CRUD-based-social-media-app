from jose import jwt
from app import schemas
from app.config import settings
import pytest

# def test_root(client):
#     res = client.get("/")
#     assert res.status_code == 200
#     assert res.json() == {"message": "Hello, World!"}

def test_create_user(client):
    res = client.post('/users/signup', json={"email": "as12@gmail.com", "password": "password123"})
    assert res.status_code == 201
    assert res.json()["email"] == "as12@gmail.com"

def test_login(client, test_user):
    res = client.post('/login', data = {"username": test_user['email'], "password": test_user['password']})
    login_res = schemas.AccessToken(**res.json())
    payload = jwt.decode(login_res.access_token , settings.secret_key, algorithms=[settings.algorithm])
    user_id: str = payload.get("user_id")

    assert user_id == test_user['id']
    assert login_res.token_type == 'bearer'
    assert res.status_code == 200

@pytest.mark.parametrize("username, password, status_code", [
    ("testuser@gmail.com", "invalidPassword", 403),
    ("invalidEmail@gmail.com", "testpass123", 403),
    ("invalidEmail@gmail.com", "invalidPassword", 403),
    (None, "testpass123", 422),
    ("testuser@gmail.com", None, 422)
])
def test_invalid_login(test_user, client, username, password, status_code):
    res = client.post('/login', data={"username" : username, "password": password})

    assert res.status_code == status_code
    # assert res.json().get('detail') == 'Invalid credentials. Please try again'