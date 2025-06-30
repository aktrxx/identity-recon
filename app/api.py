from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import crud, schemas, models

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/identify", response_model=schemas.IdentifyResponse)
def identify(payload: schemas.IdentifyRequest, db: Session = Depends(get_db)):
    email = payload.email
    phone = payload.phoneNumber
    new_contact = crud.create_contact(db, email=email, phone=phone)
    return {
            "contact": {
                "primaryContatctId": new_contact.id,
                "emails": [new_contact.email] if new_contact.email else [],
                "phoneNumbers": [new_contact.phoneNumber] if new_contact.phoneNumber else [],
                "secondaryContactIds": []
            }
    }