from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from src.database import get_db
from src.contacts import schemas, service
from src.auth.router import get_current_user
from src.auth.models import User
from fastapi_limiter.depends import RateLimiter

router = APIRouter()

@router.post("/", response_model=schemas.Contact, status_code=status.HTTP_201_CREATED, dependencies=[Depends(RateLimiter(times=5, seconds=60))])
def create_contact(contact: schemas.ContactCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return service.create_contact(db=db, contact=contact, user_id=current_user.id)

@router.get("/", response_model=List[schemas.Contact])
def read_contacts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    contacts = service.get_contacts(db, user_id=current_user.id, skip=skip, limit=limit)
    return contacts

@router.get("/{contact_id}", response_model=schemas.Contact)
def read_contact(contact_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_contact = service.get_contact(db, contact_id=contact_id, user_id=current_user.id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail={f"ID:{contact_id}": "Not Found"})
    return db_contact

@router.put("/{contact_id}", response_model=schemas.Contact)
def update_contact(contact_id: int, contact: schemas.ContactCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_contact = service.update_contact(db, contact_id=contact_id, contact=contact, user_id=current_user.id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail={f"ID:{contact_id}": "Not Found"})
    return db_contact

@router.delete("/{contact_id}", response_model=schemas.Contact)
def delete_contact(contact_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_contact = service.delete_contact(db, contact_id=contact_id, user_id=current_user.id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail={f"ID:{contact_id}": "Not Found"})
    return db_contact

@router.get("/search/", response_model=List[schemas.Contact])
def search_contacts(name: str = None, email: str = None, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    contacts = service.search_contacts(db, user_id=current_user.id, name=name, email=email)
    return contacts

@router.get("/birthdays/", response_model=List[schemas.Contact])
def contacts_with_upcoming_birthdays(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    contacts = service.get_contacts_with_upcoming_birthdays(db, user_id=current_user.id)
    return contacts
