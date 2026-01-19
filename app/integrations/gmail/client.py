from googleapiclient.discovery import build
from datetime import datetime
import base64

def fetch_latest_emails(credentials, max_results=10):
    service = build("gmail", "v1", credentials=credentials)

    results = service.users().messages().list(
        userId="me",
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

        payload = message["payload"]
        headers = payload.get("headers", [])

        subject = sender = ""
        for h in headers:
            if h["name"] == "Subject":
                subject = h["value"]
            if h["name"] == "From":
                sender = h["value"]

        body = ""
        if payload.get("body", {}).get("data"):
            body = base64.urlsafe_b64decode(
                payload["body"]["data"]
            ).decode("utf-8", errors="ignore")

        emails.append({
            "sender": sender,
            "subject": subject,
            "body": body,
            "received_at": datetime.utcnow()
        })

    return emails
