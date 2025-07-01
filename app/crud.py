from sqlalchemy.orm import Session
from app import models
from sqlalchemy import or_
from app.models import Contact

def find_related_contacts(db, email=None, phone=None):
    contacts = db.query(Contact).filter(
        or_(
            Contact.email == email,
            Contact.phoneNumber == phone
        )
    ).all()

    
    if not contacts:
        return []
    root_ids = set()
    for c in contacts:
        root_ids.add(c.id if c.linkPrecedence == "primary" else c.linkedId)
    all_related = db.query(Contact).filter(
        or_(
            Contact.id.in_(root_ids),
            Contact.linkedId.in_(root_ids)
        )
    ).all()

    return all_related



def create_contact(db: Session, email: str = None, phone: str = None, linked_id: int = None, is_primary=True):
    contact = models.Contact(
        email=email,
        phoneNumber=phone,
        linkedId=linked_id,
        linkPrecedence="primary" if is_primary else "secondary"
    )
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


def get_all_contacts(db: Session):
    return db.query(models.Contact).all()


def update_contact_to_secondary(db: Session, contact: models.Contact, primary_id: int):
    contact.linkPrecedence = "secondary"
    contact.linkedId = primary_id
    db.commit()
    db.refresh(contact)
