from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from src.database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, nullable=True)
    is_verified = Column(Boolean, default=False)
    hashed_password = Column(String)
    contacts = relationship("Contact", back_populates="owner")
