import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
from app.models import User, Session, Question, Answer
from dotenv import load_dotenv
import os

load_dotenv()

TEST_DATABASE_URL = os.environ.get("TEST_DATABASE_URL")

test_engine = create_engine(TEST_DATABASE_URL)

TestSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="function")
def db_session():
    # Create all tables fresh before each test
    Base.metadata.create_all(bind=test_engine)

    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Wipe all tables after each test - start fresh next time
        Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def client(db_session):
    # Override get_db to use test database instead of real one
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def authenticated_client(client):

    client.post("/auth/register", json={
        "name": "Test User",
        "email": "test@gmail.com",
        "password": "testpass123"
    })

    response = client.post("/auth/login", data={
        "username": "test@gmail.com",
        "password": "testpass123"
    })

    token = response.json()["access_token"]

    # Set the token on the client so all requests are authenticated
    client.headers.update({"Authorization": f"Bearer {token}"})

    return client
