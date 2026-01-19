from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.sql import func
from app.database import Base


class Email(Base):
    __tablename__ = "emails"

    id = Column(Integer, primary_key=True, index=True)

    sender = Column(String(255), nullable=False)
    subject = Column(String(500), nullable=False)

    body = Column(Text, nullable=False)
    summary = Column(Text, nullable=True)

    category = Column(String(50), nullable=True)  
    # info | action | urgent | ignore

    is_processed = Column(Boolean, default=False)

    received_at = Column(DateTime(timezone=True), server_default=func.now())
