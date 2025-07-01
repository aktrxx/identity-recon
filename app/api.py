from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import crud, schemas, models


from datetime import datetime, timedelta, timezone

FUTURE_DATE = datetime.max.replace(tzinfo=timezone.utc)

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

    related = crud.find_related_contacts(db, email=email, phone=phone)

    if not related:
        new_contact = crud.create_contact(db, email=email, phone=phone)
        return {
                "contact": {
                    "primaryContatctId": new_contact.id,
                    "emails": [new_contact.email] if new_contact.email else [],
                    "phoneNumbers": [new_contact.phoneNumber] if new_contact.phoneNumber else [],
                    "secondaryContactIds": []
                }
        }
    
    primary = min(related, key=lambda c: c.createdAt if c.linkPrecedence == "primary" else FUTURE_DATE)

    all_contacts = set()
    for contact in related:
        if contact.linkPrecedence == "primary" and contact.id != primary.id:
            crud.update_contact_to_secondary(db, contact, primary.id)
        all_contacts.add(contact)

    existing_emails = {c.email for c in all_contacts if c.email}
    existing_phones = {c.phoneNumber for c in all_contacts if c.phoneNumber}

    new_secondary = None
    if (email and email not in existing_emails) or (phone and phone not in existing_phones):
        new_secondary = crud.create_contact(db, email=email, phone=phone, linked_id=primary.id, is_primary=False)
        all_contacts.add(new_secondary)


    emails = list({c.email for c in all_contacts if c.email})
    phones = list({c.phoneNumber for c in all_contacts if c.phoneNumber})
    secondaries = [c.id for c in all_contacts if c.linkPrecedence == "secondary"]

    return {
        "contact": {
            "primaryContatctId": primary.id,
            "emails": [primary.email] + [e for e in emails if e != primary.email],
            "phoneNumbers": [primary.phoneNumber] + [p for p in phones if p != primary.phoneNumber],
            "secondaryContactIds": secondaries
        }
    }



@router.get("/contacts")
def list_all_contacts(db: Session = Depends(get_db)):
    contacts = crud.get_all_contacts(db)
    return [
        {
            "id": c.id,
            "email": c.email,
            "phoneNumber": c.phoneNumber,
            "linkedId": c.linkedId,
            "linkPrecedence": c.linkPrecedence,
            "createdAt": str(c.createdAt),
            "updatedAt": str(c.updatedAt),
            "deletedAt": str(c.deletedAt) if c.deletedAt else None
        }
        for c in contacts
    ]

@router.delete("/contacts/clear")
def clear_all_contacts(db: Session = Depends(get_db)):
    db.query(models.Contact).delete()
    db.commit()
    return {"message": "All contacts deleted successfully"}