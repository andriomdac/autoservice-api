from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from db.models.autoservice import AutoService
from schemas.autoservice import AutoServiceRequestSchema, AutoServiceResponseSchema

from db.config import get_db


autoservice_router = APIRouter(prefix="/api/autoservices")


@autoservice_router.post("/")
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


@autoservice_router.get("/", response_model=list[AutoServiceResponseSchema])
def list_autoservices(db: Session = Depends(get_db)):
    services = db.query(AutoService).all()
    return services
