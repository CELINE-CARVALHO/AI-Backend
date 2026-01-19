from sqlalchemy.orm import Session
from app.models.email import Email


def ingest_mock_emails(db: Session):
    mock_emails = [
        {
            "sender": "ceo@company.com",
            "subject": "Quarterly review",
            "body": "Prepare performance report before Friday."
        },
        {
            "sender": "hr@company.com",
            "subject": "Policy Update",
            "body": "Please review the updated leave policy."
        },
        {
            "sender": "client@external.com",
            "subject": "Urgent: Proposal Needed",
            "body": "We need the revised proposal by tomorrow EOD."
        }
    ]

    created = []

    for email_data in mock_emails:
        email = Email(**email_data)
        db.add(email)
        created.append(email)

    db.commit()

    return created
