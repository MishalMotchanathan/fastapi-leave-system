from urllib import response
import pytest
from fastapi.testclient import TestClient
from main import app
from database import SessionLocal, Base, engine
import models

# Create a fresh test DB

Base.metadata.create_all(bind=engine)

client = TestClient(app)

@pytest.fixture(autouse=True)
def run_around_tests():
    #Before each test: clear the users table
    db = SessionLocal()
    db.query(models.User).delete()
    db.commit()
    db.close()
    yield
    #After each test: Clear again
    db = SessionLocal()
    db.query(models.User).delete()
    db.commit()
    db.close()

def test_register_success():
    payload = {
        "userName":"testuser",
        "email":"testuser@example.com",
        "password":"password123"
    }
    response = client.post("/register", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "User registered Successfully"
    assert data["user"]["userName"] == "testuser"
    assert data["user"]["email"] == "testuser@example.com"
    assert "userId" in data["user"]

def test_register_existing_username_or_email():
    payload = {
        "userName": "existinguser",
        "email": "existing@example.com",
        "password": "password123"
    }
    # Register first time
    response1 = client.post("/register", json=payload)
    assert response1.status_code == 200

    # Try registering again with same username
    payload2 = {
        "userName": "existinguser",
        "email": "newemail@example.com",
        "password": "password123"
    }
    response2 = client.post("/register", json=payload2)
    assert response2.status_code == 400
    assert response2.json()["detail"] == "UserName or email already exist."

    # Try registering again with same email
    payload3 = {
        "userName": "newuser",
        "email": "existing@example.com",
        "password": "password123"
    }
    response3 = client.post("/register", json=payload3)
    assert response3.status_code == 400
    assert response3.json()["detail"] == "UserName or email already exist."

def test_register_missing_fields():
    payload = {
        "userName": "userwithoutemail",
        "password": "password123"
    }
    response = client.post("/register", json=payload)
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"][-1] == "email"
    assert response.json()["detail"][0]["msg"] == "field required"
