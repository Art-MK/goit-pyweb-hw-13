class Settings:
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost/FastAPI"
    SECRET_KEY: str = "secret_key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

settings = Settings()
