from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class EmailBase(BaseModel):
    sender: str
    subject: str
    body: str


class EmailCreate(EmailBase):
    pass


class EmailRead(EmailBase):
    id: int
    summary: Optional[str]
    category: Optional[str]
    is_processed: bool
    received_at: datetime

    class Config:
        orm_mode = True
