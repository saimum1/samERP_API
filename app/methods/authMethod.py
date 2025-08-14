from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime, timedelta
import jwt
from app.schemas.authSchema import LoginRequest

authController = APIRouter()

# Dummy database
DUMMY_USERS = [
    {
        "id": 1,
        "email": "admin@admin.com",
        "password": "admin1234",
        "name": "Admin User",
        "role": "ADMIN"
    },
    {
        "id": 2,
        "email": "towhidul015@gmail.com",
        "password": "kilobyte",
        "name": "Towhidul",
        "role": "USER"
    },
]


SECRET_KEY = "secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60




def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def login_user_method(payload: LoginRequest):

    user = next((u for u in DUMMY_USERS if u["email"] == payload.email and u["password"] == payload.password), None)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token_data = {"userId": user["id"], "email": user["email"], "role": user["role"]}
    token = create_access_token(token_data)

    return {
        "user": {
            "id": user["id"],
            "email": user["email"],
            "name": user["name"],
            "role": user["role"]
        },
        "token": token
    }
