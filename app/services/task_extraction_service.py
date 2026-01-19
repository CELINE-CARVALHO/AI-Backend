from sqlalchemy.orm import Session

from app.models.task import Task
from app.models.email import Email


def extract_task_from_email(email: Email, db: Session):
    """
    Very simple rule-based task extraction.
    This will be replaced/enhanced with AI in Step 12.
    """

    text = f"{email.subject} {email.body}".lower()

    # Basic rule: if email contains action keywords, create a task
    action_keywords = [
        "prepare",
        "submit",
        "review",
        "schedule",
        "update",
        "send",
        "complete",
        "finish"
    ]

    if not any(keyword in text for keyword in action_keywords):
        return None

    task = Task(
        title=email.subject,
        description=email.body,
        priority="high" if "urgent" in text else "medium",
        status="pending_approval",
        email_id=email.id
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task
