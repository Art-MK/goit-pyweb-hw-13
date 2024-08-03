from src.logging_config import logger
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.database import engine, Base
from src.auth import models as auth_models
from src.auth.router import router as auth_router
from src.contacts.router import router as contacts_router
from src.healthcheck.router import router as healthcheck_router

logger.info("Starting application setup")

# Create the database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI()

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from any domain, specify allowed domains in production
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Include routers
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(contacts_router, prefix="/contacts", tags=["contacts"])
app.include_router(healthcheck_router, prefix="/healthcheck", tags=["healthcheck"])

# Root endpoint
@app.get("/")
def read_root():
    logger.info("Root endpoint accessed")
    return {"message": "Welcome to my FastAPI application"}

logger.info("Application setup complete")
