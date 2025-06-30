from sqlalchemy.orm import Session
from app import models
from sqlalchemy import or_

def find_related_contacts(db: Session, email: str = None, phone: str = None):
    pass

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
