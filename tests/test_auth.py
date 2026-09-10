import pytest
import uuid

def test_root_endpoint(client):
    res = client.get("/")
    assert res.status_code == 200
    data = res.json()
    assert "status" in data
    assert data["status"] == "online"

def test_user_registration(client):
    unique_email = f"pytest_{uuid.uuid4().hex[:8]}@rentsphere.com"
    res = client.post("/users/", json={
        "email": unique_email,
        "password": "SecurePassword@123",
        "phone_number": "9123456789",
        "city": "Durgapur"
    })
    assert res.status_code == 201
    data = res.json()
    assert data["email"] == unique_email
    assert "id" in data

def test_user_login_success(client, test_user):
    res = client.post("/login", data={
        "username": test_user.email,
        "password": "TestPass@123"
    })
    assert res.status_code == 200
    data = res.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_user_login_wrong_password(client, test_user):
    res = client.post("/login", data={
        "username": test_user.email,
        "password": "WrongPassword!999"
    })
    assert res.status_code == 403
