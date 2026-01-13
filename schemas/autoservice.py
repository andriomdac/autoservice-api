from pydantic import BaseModel
from datetime import date, datetime

from schemas.payment_methods import PaymentMethodResponseSchema


class AutoServiceRequestSchema(BaseModel):
    description: str
    service_date: date
    service_value: int
    observations: str
    is_paid: bool
    tenant_id: int


class PaymentValueRequestSchema(BaseModel):
    payment_method_id: int
    amount: int


class PaymentValueResponseSchema(BaseModel):
    id: int
    payment_method_id: int
    autoservice_id: int
    amount: int
    payment_method: PaymentMethodResponseSchema

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
    payment_values: list[PaymentValueResponseSchema]

    class Config:
        from_attributes = True


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
