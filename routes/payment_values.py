from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from schemas.payment_values import PaymentValueRequestSchema
from sqlalchemy.orm import Session
from db.config import get_db


payment_value_router = APIRouter(prefix="/api/payment-values")


@payment_value_router.post("/")
def create_payment_value(
    payload: PaymentValueRequestSchema, db: Session = Depends(get_db)
):
    data = payload.model_dump()
    return data
