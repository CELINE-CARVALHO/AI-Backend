from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    priority: str = "medium"
    due_date: Optional[datetime] = None
    email_id: Optional[int] = None


class TaskCreate(TaskBase):
    pass


class TaskRead(BaseModel):
    id: int
    title: str

    model_config = {
        "from_attributes": True
    }

