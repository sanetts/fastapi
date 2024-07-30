from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from pydantic import BaseModel, EmailStr
from app.database import get_db
from passlib.context import CryptContext

router = APIRouter()

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

# Dependency to hash passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

@router.post("/register/")
async def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.execute(
        text("SELECT * FROM users WHERE email = :email"),
        {"email": user.email}
    ).fetchone()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(user.password)
    db.execute(
        text("INSERT INTO users (username, email, hashed_password) VALUES (:username, :email, :hashed_password)"),
        {"username": user.username, "email": user.email, "hashed_password": hashed_password}
    )
    db.commit()

    # Return the user details along with a success message
    return {"message": "User registered successfully", "username": user.username, "email": user.email}
