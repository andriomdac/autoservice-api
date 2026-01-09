from pydantic import BaseModel


class PaymentValueRequestSchema(BaseModel):
    payment_method: str
    autoservice: str
    amount: int
