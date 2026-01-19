from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.api.dependencies import get_db
from app.models.task import Task
from app.schemas.task import TaskRead

router = APIRouter()


# GET all tasks
@router.get("/", response_model=List[TaskRead])
def get_tasks(db: Session = Depends(get_db)):
    return db.query(Task).order_by(Task.created_at.desc()).all()


# GET pending approval tasks
@router.get("/pending", response_model=List[TaskRead])
def get_pending_tasks(db: Session = Depends(get_db)):
    return db.query(Task).filter(Task.status == "pending_approval").all()


# APPROVE task
@router.post("/{task_id}/approve")
def approve_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.status = "approved"
    db.commit()

    return {
        "message": "Task approved",
        "task_id": task.id
    }


# REJECT task
@router.post("/{task_id}/reject")
def reject_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.status = "rejected"
    db.commit()

    return {
        "message": "Task rejected",
        "task_id": task.id
    }
