from pydantic import BaseModel


class PaymentValueRequestSchema(BaseModel):
    payment_method_id: int
    autoservice_id: int
    amount: int
