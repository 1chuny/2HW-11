from sqlalchemy.orm import Session
from models import Contact
from schemas import ContactCreate

def get_contact(db: Session, contact_id: int):
    return db.query(Contact).filter(Contact.id == contact_id).first()

def get_contacts(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Contact).offset(skip).limit(limit).all()

def create_contact(db: Session, contact: ContactCreate):
    db_contact = Contact(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def delete_contact(db: Session, contact_id: int):
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    db.delete(db_contact)
    db.commit()
    return db_contact

def update_contact(db: Session, contact_id: int, contact: ContactCreate):
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    for key, value in contact.dict().items():
        setattr(db_contact, key, value)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def search_contacts(db: Session, query: str):
    return db.query(Contact).filter(
        (Contact.first_name.ilike(f'%{query}%')) |
        (Contact.last_name.ilike(f'%{query}%')) |
        (Contact.email.ilike(f'%{query}%'))
    ).all()

def get_upcoming_birthdays(db: Session):
    from datetime import datetime, timedelta
    today = datetime.today()
    next_week = today + timedelta(days=7)
    return db.query(Contact).filter(Contact.birthday.between(today, next_week)).all()
