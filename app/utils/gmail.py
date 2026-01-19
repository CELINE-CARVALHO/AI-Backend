from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import base64
from typing import List, Dict


def get_gmail_service(user) -> object:
    """
    Creates and returns a Gmail API service using stored OAuth credentials.
    """

    # Build credentials object from DB values
    creds = Credentials(
        token=user.access_token,
        refresh_token=user.refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=user.google_client_id,
        client_secret=user.google_client_secret,
        scopes=["https://www.googleapis.com/auth/gmail.readonly"],
    )

    # Refresh token if expired
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())

    # Create Gmail service
    service = build("gmail", "v1", credentials=creds)

    return service


def fetch_inbox_emails(user, max_results: int = 5) -> List[Dict]:
    """
    Fetches latest inbox emails and returns basic details.
    """

    service = get_gmail_service(user)

    results = service.users().messages().list(
        userId="me",
        labelIds=["INBOX"],
        maxResults=max_results
    ).execute()

    messages = results.get("messages", [])
    emails = []

    for msg in messages:
        message = service.users().messages().get(
            userId="me",
            id=msg["id"],
            format="full"
        ).execute()

        headers = message["payload"].get("headers", [])

        subject = next((h["value"] for h in headers if h["name"] == "Subject"), "")
        sender = next((h["value"] for h in headers if h["name"] == "From"), "")
        date = next((h["value"] for h in headers if h["name"] == "Date"), "")

        body = ""

        payload = message["payload"]
        if "parts" in payload:
            for part in payload["parts"]:
                if part["mimeType"] == "text/plain" and "data" in part["body"]:
                    body = base64.urlsafe_b64decode(
                        part["body"]["data"]
                    ).decode("utf-8", errors="ignore")
                    break
        elif "data" in payload.get("body", {}):
            body = base64.urlsafe_b64decode(
                payload["body"]["data"]
            ).decode("utf-8", errors="ignore")

        emails.append({
            "gmail_message_id": msg["id"],
            "subject": subject,
            "sender": sender,
            "date": date,
            "body": body[:500]  # limit body for safety
        })

    return emails
