from pydantic import BaseModel
from datetime import date, datetime


class AutoServiceResponseSchema(BaseModel):
    uuid: str
    description: str
    service_date: date
    service_value: int
    observations: str
    is_paid: bool
    created_at: datetime


class AutoServiceRequestSchema(BaseModel):
    description: str
    service_date: date
    service_value: int
    observations: str
    is_paid: bool
