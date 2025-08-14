from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime, timedelta
import jwt
from app.methods import authMethod
from app.schemas.authSchema import LoginRequest

# Router for /user routes
authController = APIRouter()

@authController.post("/login")
def login_user(payload: LoginRequest):
    return authMethod.login_user_method(payload)
   