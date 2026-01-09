from pydantic import BaseModel


class PaymentValueRequestSchema(BaseModel):
    payment_method: int
    autoservice: int
    amount: int
