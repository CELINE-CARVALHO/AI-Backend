from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from google.oauth2 import id_token
from google.auth.transport import requests
import os
import jwt
from datetime import datetime, timedelta

router = APIRouter(prefix="/auth", tags=["Auth"])

JWT_SECRET = os.getenv("JWT_SECRET")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")


class GoogleTokenRequest(BaseModel):
    token: str


@router.post("/google")
def google_login(data: GoogleTokenRequest):
    try:
        # Verify Google ID token
        idinfo = id_token.verify_oauth2_token(
            data.token,
            requests.Request(),
            GOOGLE_CLIENT_ID,
        )

        email = idinfo["email"]
        name = idinfo.get("name", "")

        # Create JWT for frontend
        payload = {
            "email": email,
            "name": name,
            "exp": datetime.utcnow() + timedelta(hours=24),
        }

        access_token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")

        return {
            "access_token": access_token,
            "user": {
                "email": email,
                "name": name,
            },
        }

    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid Google token")
