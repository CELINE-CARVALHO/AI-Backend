from fastapi import APIRouter, Depends
from app.core.auth import get_current_user
from datetime import date

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/daily-summary")
def daily_summary(user=Depends(get_current_user)):
    # TEMP: mock data (we replace later)
    return {
        "date": date.today().isoformat(),
        "emails_today": [],
        "pending_tasks": [],
        "approved_tasks": [],
        "calendar_events": [],
    }
