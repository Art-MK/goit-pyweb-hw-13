from pydantic import BaseModel

class HealthCheckResponse(BaseModel):
    status: str
    details: str = None
