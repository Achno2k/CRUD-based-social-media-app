''' Conftest.py is a special type of file which is used by pytest in order to define all the fixtures 
in a single file which is accessible across the whole test directory, so we dont have to import any fixture  '''

import pytest
from fastapi.testclient import TestClient
from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.config import settings
from app.oauth2 import create_token
from app import models

SQLALCHEMY_TESTDB_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}_testing'

engine = create_engine(SQLALCHEMY_TESTDB_URL, pool_pre_ping=True)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# # Create all tables in the test database
# Base.metadata.create_all(bind=engine)

# client = TestClient(app)


# Run our code before we run our test, e.g - create tables
# Get that database dependency and perform the tests
# Run some code after our test finishes, e.g - drop all the tables

@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

@pytest.fixture
def test_user(client):
    user_data = {"email": "testuser1@gmail.com", "password": "testpass123"}
    res = client.post("/users/signup", json=user_data)
    new_user = res.json()           # json = {id: , email: , created_at: }, just like our UserOut schema 
    new_user['password'] = user_data['password']    # adding a password feild as well which can be used when we will login with this user
    return new_user         # return this user

@pytest.fixture
def test_user2(client):
    user_data = {"email": "testuser2@gmail.com", "password": "testpass123"}
    res = client.post("/users/signup", json=user_data)
    new_user = res.json()          
    new_user['password'] = user_data['password']  
    return new_user

@pytest.fixture
def token(test_user):
    token = create_token({"user_id": test_user['id']})
    return token

@pytest.fixture
def authorized_client(token, client):
    client.headers = {
        **client.headers,
        "Authorization" : f"Bearer {token}"
    }
    return client

def create_post_model(post):
    new_post = models.Post(**post)
    return new_post

@pytest.fixture
def test_posts(test_user, session, test_user2):
    posts_data = [{
        "title": "First title",
        "content": "First content",
        "owner_id": test_user['id']
    }, {
        "title": "Second title",
        "content": "Second content",
        "owner_id": test_user['id']
    }, {
        "title": "Third title",
        "content": "Third content",
        "owner_id": test_user['id']
    }, {
        "title": "Fourth title",
        "content": "Fourth content",
        "owner_id": test_user2['id']
    }]

    test_posts_list = list(map(create_post_model, posts_data))
    session.add_all(test_posts_list)
    session.commit()
    posts = session.query(models.Post).all()
    return posts


