from pydantic import BaseModel


class PaymentMethodRequestSchema(BaseModel):
    name: str


class PaymentMethodResponseSchema(BaseModel):
    id: int
    name: str
