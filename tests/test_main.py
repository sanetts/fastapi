from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_user():
    response = client.post(
        "/register/",
        json={"username": "testuser", "email": "testuser@example.com", "password": "testpassword"}
    )
    assert response.status_code == 200, response.text  # Print response text for debugging
    data = response.json()
    assert data["message"] == "User registered successfully"
    assert data["username"] == "testuser"
    assert data["email"] == "testuser@example.com"



def test_login_user():
    # Check if the user already exists
    check_user_response = client.get(
        "/check-user/",
        params={"email": "testuser@example.com"}
    )
    
    if check_user_response.status_code == 200:
        user_exists = check_user_response.json().get("exists", False)
        
        if not user_exists:
            # Register the user if they don't exist
            register_response = client.post(
                "/register/",
                json={"username": "testuser", "email": "testuser@example.com", "password": "testpassword"}
            )
            assert register_response.status_code == 200

    # Now login with the registered or newly registered user
    login_response = client.post(
        "/login/",
        json={"email": "testuser@example.com", "password": "testpassword"}
    )
    assert login_response.status_code == 200
    login_data = login_response.json()
    assert "access_token" in login_data  
    assert login_data["token_type"] == "bearer"