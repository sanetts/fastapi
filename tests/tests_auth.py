from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_user():
    response = client.post("/register/", json={"username": "testuser", "email": "testuser@example.com", "password": "password"})
    assert response.status_code == 200
    assert response.json()["email"] == "testuser@example.com"

def test_login():
    response = client.post("/login/", json={"username": "testuser", "password": "password"})
    assert response.status_code == 200
    assert "access_token" in response.json()


