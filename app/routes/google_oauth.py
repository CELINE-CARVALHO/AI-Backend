from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from datetime import datetime
import os

from app.database import SessionLocal
from app.models.oauth_token import OAuthToken

router = APIRouter(
    prefix="/auth/google",
    tags=["Google OAuth"]
)

# =========================
# ENV VARIABLES
# =========================
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

REDIRECT_URI = "http://localhost:8000/auth/google/callback"

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly"
]

# =========================
# DATABASE DEPENDENCY
# =========================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# =========================
# LOGIN → GOOGLE CONSENT
# =========================
@router.get("/login")
def google_login():
    if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
        raise HTTPException(
            status_code=500,
            detail="Google OAuth environment variables not set"
        )

    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        },
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI,
    )

    auth_url, _ = flow.authorization_url(
        access_type="offline",
        prompt="consent"
    )

    return RedirectResponse(auth_url)

# =========================
# CALLBACK → TOKEN EXCHANGE
# =========================
@router.get("/callback")
def google_callback(code: str, db: Session = Depends(get_db)):
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        },
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI,
    )

    flow.fetch_token(code=code)
    creds: Credentials = flow.credentials

    token_entry = OAuthToken(
        email="temp_user@gmail.com",  # replace later
        access_token=creds.token,
        refresh_token=creds.refresh_token,
        token_expiry=creds.expiry,
    )

    db.add(token_entry)
    db.commit()

    return {
        "message": "Google OAuth successful. Gmail permission granted."
    }
