from pydantic import BaseModel


class AutoServiceRequestSchema(BaseModel):
    uuid: str
    description: str
    service_date: int
    service_value: int
    observations: str
    is_paid: bool
    created_at: str
