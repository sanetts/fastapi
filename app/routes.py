from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from pydantic import BaseModel, EmailStr
from app.database import get_db
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta

router = APIRouter()

# Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_jwt_token(email: str):
    expiration = datetime.utcnow() + timedelta(hours=1)
    token = jwt.encode({"sub": email, "exp": expiration}, "your_secret_key", algorithm="HS256")
    return token

# Pydantic models
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Register endpoint
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

# Login endpoint
@router.post("/login/")
async def login(user: UserLogin, db: Session = Depends(get_db)):
    result = db.execute(
        text("SELECT * FROM users WHERE email = :email"),
        {"email": user.email}
    ).fetchone()

    if result is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Assuming the result is a tuple and hashed_password is in the third column
    hashed_password = result[2]  # Adjust this index according to your table schema

    if not verify_password(user.password, hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_jwt_token(user.email)
    return {"access_token": token, "token_type": "bearer"}
