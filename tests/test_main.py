from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_user():
    response = client.post(
        "/register/",
        json={"username": "testuser", "email": "testuser@example.com", "password": "testpassword"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "User registered successfully"
    assert data["username"] == "testuser"
    assert data["email"] == "testuser@example.com"
