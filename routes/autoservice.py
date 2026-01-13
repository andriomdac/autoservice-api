from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from db.models.autoservice import AutoService, PaymentMethod, PaymentValue
from schemas.autoservice import (
    AutoServiceDetailResponseSchema,
    AutoServiceRequestSchema,
    AutoServiceResponseSchema,
    PaymentValueRequestSchema,
    PaymentValueResponseSchema,
)
from db.config import get_db


autoservice_router = APIRouter(prefix="/api/autoservices")


@autoservice_router.post("/", response_model=AutoServiceResponseSchema, status_code=201)
def create_autoservice(
    payload: AutoServiceRequestSchema, db: Session = Depends(get_db)
):
    data = payload.model_dump(mode="python")
    autoservice = AutoService(**data)

    service_exists = (
        db.query(AutoService)
        .filter(
            AutoService.description == autoservice.description,
            AutoService.service_date == autoservice.service_date,
        )
        .first()
    )
    if service_exists:
        raise HTTPException(
            409,
            f"Serviço com essa descrição ({autoservice.description}) já existe para essa data.",
        )

    db.add(autoservice)
    db.commit()
    db.refresh(autoservice)

    return autoservice


@autoservice_router.get("/", response_model=list[AutoServiceDetailResponseSchema])
def list_autoservices(db: Session = Depends(get_db)):
    services = db.query(AutoService).all()
    return services


@autoservice_router.get(
    "/{autoservice_id}/", response_model=AutoServiceDetailResponseSchema
)
def detail_autoservice(autoservice_id: int, db: Session = Depends(get_db)):
    autoservice_exists = (
        db.query(AutoService).filter(AutoService.id == autoservice_id).first()
    )
    if not autoservice_exists:
        raise HTTPException(404, "Serviço não encontrado")

    return autoservice_exists


@autoservice_router.post(
    "/{autoservice_id}/values/",
    response_model=PaymentValueResponseSchema,
    status_code=201,
)
def add_autoservice_value(
    payload: PaymentValueRequestSchema,
    autoservice_id: int,
    db: Session = Depends(get_db),
):
    # Etapa 1: Método de pagamento existe no banco?
    method_exists = (
        db.query(PaymentMethod)
        .filter(PaymentMethod.id == payload.payment_method_id)
        .first()
    )
    if not method_exists:
        raise HTTPException(404, "Método de Pagamento não encontrado")

    # Etapa 2: O serviço (autoservice) existe no banco?
    autoservice_exists = (
        db.query(AutoService).filter(AutoService.id == autoservice_id).first()
    )
    if not autoservice_exists:
        raise HTTPException(404, "Serviço não encontrado")

    # Etapa 3: O método de pagamento utilizado pra este novo valor já existe em algum
    # dos valores atrelados a esse serviço?
    value_method_exists = (
        db.query(PaymentValue)
        .filter(
            PaymentValue.autoservice_id == autoservice_id,
            PaymentValue.payment_method_id == payload.payment_method_id,
        )
        .first()
    )
    if value_method_exists:
        raise HTTPException(409, "Este método de pagamento já existe para esse serviço")

    # Etapa 4: Montar o objeto Value utilizando as informações dadas pelo usuário
    new_value = PaymentValue(**payload.model_dump(), autoservice_id=autoservice_id)

    # Etapa 5: Salvar o novo objeto no banco
    db.add(new_value)
    db.commit()
    db.refresh(new_value)

    return new_value
