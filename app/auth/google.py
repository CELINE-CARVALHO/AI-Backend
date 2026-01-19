from google.oauth2 import id_token
from google.auth.transport import requests
from fastapi import HTTPException
import os

def verify_google_token(token: str):
    try:
        idinfo = id_token.verify_oauth2_token(
            token,
            requests.Request(),
            os.getenv("GOOGLE_CLIENT_ID")
        )
        print("GOOGLE TOKEN VERIFIED:", idinfo)
        return idinfo
    except Exception as e:
        print("GOOGLE TOKEN ERROR:", e)
        raise HTTPException(status_code=401, detail="Invalid Google token")

