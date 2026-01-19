from fastapi import APIRouter
from pydantic import BaseModel
from app.auth.google import verify_google_token
from jose import jwt
import os
from datetime import datetime, timedelta
import os
print("JWT_SECRET:", os.getenv("JWT_SECRET"))
router = APIRouter()

class GoogleAuthRequest(BaseModel):
    token: str

@router.post("/auth/google")
def google_auth(data: GoogleAuthRequest):
    user_info = verify_google_token(data.token)

    payload = {
        "email": user_info["email"],
        "name": user_info["name"],
        "exp": datetime.utcnow() + timedelta(hours=24)
    }

    access_token = jwt.encode(
        payload,
        os.getenv("JWT_SECRET"),
        algorithm="HS256"
    )

    return {
        "access_token": access_token,
        "user": payload
    }
