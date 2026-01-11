from pydantic import BaseModel
from datetime import date, datetime


class AutoServiceResponseSchema(BaseModel):
    id: int
    description: str
    service_date: date
    service_value: int
    observations: str
    is_paid: bool
    created_at: datetime

    class Config:
        from_attributes = True


class AutoServiceRequestSchema(BaseModel):
    description: str
    service_date: date
    service_value: int
    observations: str
    is_paid: bool


class PaymentValueRequestSchema(BaseModel):
    payment_method_id: int
    amount: int


class PaymentValueResponseSchema(BaseModel):
    id: int
    payment_method_id: int
    autoservice_id: int
    amount: int

    class Config:
        from_attributes = True


class AutoServiceDetailResponseSchema(BaseModel):
    id: int
    description: str
    service_date: date
    service_value: int
    observations: str
    is_paid: bool
    created_at: datetime
    values: list
