# test_connection.py
from app.database import SessionLocal

def test_connection():
    try:
        db = SessionLocal()
        print("Database connection successful")
    except Exception as e:
        print(f"Database connection failed: {e}")

if __name__ == "__main__":
    test_connection()
