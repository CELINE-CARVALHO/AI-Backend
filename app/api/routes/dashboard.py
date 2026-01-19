from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date

from app.api.dependencies import get_db
from app.models.email import Email
from app.models.task import Task
from app.models.calendar import CalendarEvent
from app.services.ai_summary_service import summarize_text

router = APIRouter()


@router.get("/daily-summary")
def daily_executive_summary(db: Session = Depends(get_db)):
    today = date.today()

    # ---------------------------
    # Emails with AI summary
    # ---------------------------
    emails_today = db.query(Email).order_by(Email.received_at.desc()).all()

    emails_with_summary = []
    for e in emails_today:
        summary = summarize_text(f"{e.subject}. {e.body}")
        emails_with_summary.append({
            "id": e.id,
            "sender": e.sender,
            "subject": e.subject,
            "summary": summary,
            "received_at": e.received_at
        })

    # ---------------------------
    # Pending tasks
    # ---------------------------
    pending_tasks = (
        db.query(Task)
        .filter(Task.status == "pending_approval")
        .all()
    )

    # ---------------------------
    # Approved tasks
    # ---------------------------
    approved_tasks = (
        db.query(Task)
        .filter(Task.status == "approved")
        .all()
    )

    # ---------------------------
    # Calendar events
    # ---------------------------
    calendar_events = db.query(CalendarEvent).all()

    # ---------------------------
    # Final executive response
    # ---------------------------
    return {
        "date": today.isoformat(),
        "emails_today": emails_with_summary,
        "pending_tasks": [
            {
                "id": t.id,
                "title": t.title,
                "priority": t.priority,
            }
            for t in pending_tasks
        ],
        "approved_tasks": [
            {
                "id": t.id,
                "title": t.title,
                "priority": t.priority,
            }
            for t in approved_tasks
        ],
        "calendar_events": [
            {
                "id": c.id,
                "title": c.title,
                "start_time": c.start_time,
                "end_time": c.end_time,
            }
            for c in calendar_events
        ],
    }
