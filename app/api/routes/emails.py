from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from typing import List

from app.api.dependencies import get_db
from app.models.email import Email
from app.schemas.email import EmailCreate, EmailRead
from app.services.email_service import ingest_mock_emails
from app.services.task_extraction_service import extract_task_from_email

from app.integrations.gmail.oauth import get_oauth_flow
from app.integrations.gmail.client import fetch_latest_emails
from app.integrations.gmail.parser import save_emails


router = APIRouter()

# =========================================================
# GMAIL OAUTH (⚠️ MUST BE BEFORE /{email_id} ROUTES)
# =========================================================

@router.get("/gmail/connect")
def gmail_connect():
    flow = get_oauth_flow()
    auth_url, _ = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true"
    )
    return RedirectResponse(auth_url)


@router.get("/gmail/callback")
def gmail_callback(request: Request, db: Session = Depends(get_db)):
    flow = get_oauth_flow()
    flow.fetch_token(authorization_response=str(request.url))

    credentials = flow.credentials
    emails = fetch_latest_emails(credentials)
    saved = save_emails(db, emails)

    return {
        "message": "Gmail synced successfully",
        "emails_saved": len(saved),
    }


# =========================================================
# EMAIL CRUD
# =========================================================

@router.post("/", response_model=EmailRead)
def create_email(email: EmailCreate, db: Session = Depends(get_db)):
    db_email = Email(
        sender=email.sender,
        subject=email.subject,
        body=email.body,
    )
    db.add(db_email)
    db.commit()
    db.refresh(db_email)
    return db_email


@router.get("/", response_model=List[EmailRead])
def get_emails(db: Session = Depends(get_db)):
    return db.query(Email).order_by(Email.received_at.desc()).all()


@router.get("/{email_id}", response_model=EmailRead)
def get_email(email_id: int, db: Session = Depends(get_db)):
    email = db.query(Email).filter(Email.id == email_id).first()
    if not email:
        raise HTTPException(status_code=404, detail="Email not found")
    return email


# =========================================================
# MOCK INGESTION
# =========================================================

@router.post("/mock-ingest")
def mock_ingest(db: Session = Depends(get_db)):
    emails = ingest_mock_emails(db)
    return {
        "inserted": len(emails),
        "message": "Mock emails ingested successfully",
    }


# =========================================================
# EMAIL → TASK EXTRACTION
# =========================================================

@router.post("/{email_id}/extract-task")
def extract_task(email_id: int, db: Session = Depends(get_db)):
    email = db.query(Email).filter(Email.id == email_id).first()

    if not email:
        raise HTTPException(status_code=404, detail="Email not found")

    task = extract_task_from_email(email, db)

    if not task:
        return {
            "message": "Email is not actionable, no task created",
        }

    return {
        "message": "Task created from email",
        "task_id": task.id,
        "priority": task.priority,
    }
