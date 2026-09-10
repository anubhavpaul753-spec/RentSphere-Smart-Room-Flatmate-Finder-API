import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app import models, utils, oauth2

@pytest.fixture(scope="session")
def client():
    return TestClient(app)

@pytest.fixture(scope="session")
def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def test_user(db_session):
    email = "test.pytest.user@rentsphere.com"
    user = db_session.query(models.User).filter(models.User.email == email).first()
    if not user:
        user = models.User(
            email=email,
            password=utils.hash("TestPass@123"),
            phone_number="9998887776",
            city="Durgapur"
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
    return user

@pytest.fixture
def auth_headers(test_user):
    token = oauth2.create_access_token({"user_id": test_user.id})
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def secondary_user(db_session):
    email = "secondary.pytest.user@rentsphere.com"
    user = db_session.query(models.User).filter(models.User.email == email).first()
    if not user:
        user = models.User(
            email=email,
            password=utils.hash("SecPass@123"),
            phone_number="9998881112",
            city="Kolkata"
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
    return user

@pytest.fixture
def secondary_auth_headers(secondary_user):
    token = oauth2.create_access_token({"user_id": secondary_user.id})
    return {"Authorization": f"Bearer {token}"}
