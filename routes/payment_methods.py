from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from db.config import get_db
from db.models.autoservice import PaymentMethod
from schemas.payment_methods import (
    PaymentMethodRequestSchema,
    PaymentMethodResponseSchema,
)
from utils.security import token_required

payment_method_router = APIRouter(prefix="/api/payment-methods")


@payment_method_router.get(
    "/",
    response_model=list[PaymentMethodResponseSchema],
    dependencies=[Depends(token_required)],
)
def list_methods(db: Session = Depends(get_db)):
    methods = db.query(PaymentMethod).all()
    return methods


@payment_method_router.post(
    "/",
    response_model=PaymentMethodResponseSchema,
    dependencies=[Depends(token_required)],
)
def create_method(payload: PaymentMethodRequestSchema, db: Session = Depends(get_db)):
    data = payload.model_dump()
    method = PaymentMethod()
    method.name = data["name"]

    method_exists = (
        db.query(PaymentMethod).filter(PaymentMethod.name == method.name).first()
    )
    if method_exists:
        raise HTTPException(409, f"Método '{method.name}' já existe")

    db.add(method)
    db.commit()
    db.refresh(method)

    return method
