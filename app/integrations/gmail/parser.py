from app.models.email import Email

def save_emails(db, email_data):
    saved = []
    for e in email_data:
        email = Email(
            sender=e["sender"],
            subject=e["subject"],
            body=e["body"]
        )
        db.add(email)
        saved.append(email)

    db.commit()
    return saved
