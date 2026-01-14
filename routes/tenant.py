from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.config import get_db
from schemas.tenant import TenantRequestSchema, TenantResponseSchema
from db.models.tenant import Tenant
from utils.security import token_required

tenant_router = APIRouter(prefix="/api/tenants")


@tenant_router.post(
    "/",
    response_model=TenantResponseSchema,
    status_code=201,
    dependencies=[Depends(token_required)],
)
def create_tenant(payload: TenantRequestSchema, db: Session = Depends(get_db)):
    tenant_exists = db.query(Tenant).filter(Tenant.name == payload.name).first()
    if tenant_exists:
        raise HTTPException(409, "Empresa com mesmo nome já existe")

    tenant_obj = Tenant(**payload.model_dump())

    db.add(tenant_obj)
    db.commit()
    db.refresh(tenant_obj)

    return tenant_obj


@tenant_router.get(
    "/",
    response_model=list[TenantResponseSchema],
    dependencies=[Depends(token_required)],
)
def list_tenants(db: Session = Depends(get_db)):
    tenants = db.query(Tenant).all()
    return tenants
