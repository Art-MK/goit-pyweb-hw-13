import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.config import settings

DATABASE_URL = settings.DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Check database connection
def check_db_connection():
    try:
        with engine.connect() as connection:
            logging.info("Successfully connected to the database.")
    except Exception as e:
        logging.error(f"Database connection failed: {e}")
        raise

# Get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Check database connection on startup
check_db_connection()
