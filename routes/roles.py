from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.config import get_db
from db.models.users import Role
from schemas.roles import RoleRequestSchema, RoleResponseSchema
from utils.security import token_required


role_router = APIRouter(prefix="/api/roles")


@role_router.get(
    "/", dependencies=[Depends(token_required)], response_model=list[RoleResponseSchema]
)
def list_roles(db: Session = Depends(get_db)):
    roles = db.query(Role).all()
    return roles


@role_router.post(
    "/", dependencies=[Depends(token_required)], response_model=RoleResponseSchema
)
def create_role(payload: RoleRequestSchema, db: Session = Depends(get_db)):
    role_exists = db.query(Role).filter(Role.name == payload.name).first()
    if role_exists:
        raise HTTPException(401, "Permissão já existe")
    role = Role(**payload.model_dump())

    db.add(role)
    db.commit()
    db.refresh(role)
    return role
