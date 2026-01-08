from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from schemas.autoservice import AutoServiceRequestSchema

from db.config import get_db


autoservice_router = APIRouter(prefix="/api/autoservices")


@autoservice_router.post("/")
def create_autoservice(
    payload: AutoServiceRequestSchema, db: Session = Depends(get_db)
):
    return payload
