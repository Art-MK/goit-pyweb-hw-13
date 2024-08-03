from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.database import get_db
from src.healthcheck.schemas import HealthCheckResponse
from src.database import check_db_connection

router = APIRouter()

@router.get("/", response_model=HealthCheckResponse)
def health_check(db: Session = Depends(get_db)):
    try:
        check_db_connection()
        return {"status": "ok"}
    except Exception as e:
        return {"status": "unhealthy", "details": str(e)}
