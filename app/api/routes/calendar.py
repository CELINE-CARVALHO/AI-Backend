from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.api.dependencies import get_db
from app.models.task import Task
from app.models.calendar import CalendarEvent

router = APIRouter()


# ---------------------------
# GET all calendar events
# ---------------------------
@router.get("/")
def get_calendar_events(db: Session = Depends(get_db)):
    events = db.query(CalendarEvent).order_by(CalendarEvent.start_time).all()

    return [
        {
            "id": e.id,
            "title": e.title,
            "start_time": e.start_time,
            "end_time": e.end_time
        }
        for e in events
    ]


# ---------------------------
# SCHEDULE approved task
# ---------------------------
@router.post("/schedule/{task_id}")
def schedule_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.status != "approved":
        raise HTTPException(status_code=400, detail="Task not approved")

    start_time = datetime.utcnow() + timedelta(hours=1)
    end_time = start_time + timedelta(hours=1)

    event = CalendarEvent(
        task_id=task.id,
        title=task.title,
        start_time=start_time,
        end_time=end_time
    )

    db.add(event)
    db.commit()
    db.refresh(event)

    return {
        "message": "Task scheduled",
        "event_id": event.id,
        "start_time": start_time,
        "end_time": end_time
    }
