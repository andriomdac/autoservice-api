from pydantic import BaseModel


class PaymentMethodRequestSchema(BaseModel):
    name: str


class PaymentMethodResponseSchema(BaseModel):
    uuid: str
    name: str
