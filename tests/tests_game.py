from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_game():
    login_response = client.post("/login/", json={"username": "testuser", "password": "password"})
    token = login_response.json().get("access_token")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.post("/games/", json={"game_type": "Football", "location": "Stadium", "stadium_name": "Main Stadium", "game_date": "2024-01-01", "number_of_players": 22}, headers=headers)
    assert response.status_code == 200
    assert response.json()["game_type"] == "Football"

def test_read_game():
    login_response = client.post("/login/", json={"username": "testuser", "password": "password"})
    token = login_response.json().get("access_token")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Assuming the game with ID 1 exists
    response = client.get("/games/1", headers=headers)
    assert response.status_code == 200
