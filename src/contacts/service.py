from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from src.contacts import models, schemas
from datetime import datetime, timedelta
from src.logging_config import logger

def create_contact(db: Session, contact: schemas.ContactCreate, user_id: int):
    try:
        db_contact = models.Contact(**contact.model_dump(), user_id=user_id)
        db.add(db_contact)
        db.commit()
        db.refresh(db_contact)
        logger.info(f"Contact created: {db_contact.id} for user: {user_id}")
        return db_contact
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Error creating contact for user {user_id}: {e}")
        raise HTTPException(status_code=409, detail="Contact with this email already exists")
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating contact for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Error creating contact")

def get_contacts(db: Session, user_id: int, skip: int = 0, limit: int = 10):
    try:
        contacts = db.query(models.Contact).filter(models.Contact.user_id == user_id).offset(skip).limit(limit).all()
        logger.info(f"Retrieved {len(contacts)} contacts for user: {user_id}")
        return contacts
    except Exception as e:
        logger.error(f"Error retrieving contacts for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving contacts")

def get_contact(db: Session, contact_id: int, user_id: int) -> models.Contact:
    try:
        contact = db.query(models.Contact).filter(models.Contact.id == contact_id, models.Contact.user_id == user_id).first()
        if contact:
            logger.info(f"Contact retrieved: {contact.id} for user: {user_id}")
        else:
            logger.info(f"No contact found with ID {contact_id} for user {user_id}")
        return contact
    except Exception as e:
        logger.error(f"Error retrieving contact {contact_id} for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving contact")

def update_contact(db: Session, contact_id: int, contact: schemas.ContactUpdate, user_id: int) -> models.Contact:
    try:
        db_contact = db.query(models.Contact).filter(models.Contact.id == contact_id, models.Contact.user_id == user_id).first()
        if db_contact is None:
            logger.info(f"No contact found with ID {contact_id} for user {user_id}")
            return None
        for key, value in contact.model_dump().items():
            setattr(db_contact, key, value)
        db.commit()
        db.refresh(db_contact)
        logger.info(f"Contact updated: {db_contact.id} for user: {user_id}")
        return db_contact
    except Exception as e:
        logger.error(f"Error updating contact {contact_id} for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Error updating contact")

def delete_contact(db: Session, contact_id: int, user_id: int) -> models.Contact:
    try:
        db_contact = db.query(models.Contact).filter(models.Contact.id == contact_id, models.Contact.user_id == user_id).first()
        if db_contact is None:
            logger.info(f"No contact found with ID {contact_id} for user {user_id}")
            return None
        db.delete(db_contact)
        db.commit()
        logger.info(f"Contact deleted: {db_contact.id} for user: {user_id}")
        return db_contact
    except Exception as e:
        logger.error(f"Error deleting contact {contact_id} for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Error deleting contact")

def search_contacts(db: Session, user_id: int, name: str = None, email: str = None):
    try:
        query = db.query(models.Contact).filter(models.Contact.user_id == user_id)
        if name:
            query = query.filter((models.Contact.first_name.ilike(f"%{name}%")) | (models.Contact.last_name.ilike(f"%{name}%")))
        if email:
            query = query.filter(models.Contact.email.ilike(f"%{email}%"))
        contacts = query.all()
        logger.info(f"Found {len(contacts)} contacts matching criteria for user: {user_id}")
        return contacts
    except Exception as e:
        logger.error(f"Error searching contacts for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Error searching contacts")

def get_contacts_with_upcoming_birthdays(db: Session, user_id: int):
    try:
        today = datetime.today()
        upcoming = today + timedelta(days=7)
        contacts = db.query(models.Contact).filter(
            models.Contact.user_id == user_id,
            models.Contact.birthday.between(today, upcoming)
        ).all()
        logger.info(f"Found {len(contacts)} contacts with upcoming birthdays for user: {user_id}")
        return contacts
    except Exception as e:
        logger.error(f"Error retrieving contacts with upcoming birthdays for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving contacts with upcoming birthdays")
