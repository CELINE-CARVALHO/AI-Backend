from app.database import engine
from app.models import email

email.Base.metadata.create_all(bind=engine)
