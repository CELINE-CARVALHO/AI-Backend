from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from app.database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

    priority = Column(String(20), default="medium")
    # low | medium | high | urgent

    status = Column(String(30), default="pending_approval")
    # pending_approval | approved | rejected | completed

    due_date = Column(DateTime, nullable=True)

    email_id = Column(Integer, ForeignKey("emails.id"), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)
