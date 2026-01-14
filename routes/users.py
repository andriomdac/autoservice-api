from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.models.tenant import Tenant
from schemas.users import (
    UserAdminCreateSchema,
    UserResponseSchema,
    UserUpdateSchema,
)
from db.models.users import Role, User
from db.config import get_db
from utils.security import authenticate_user, get_password_hash, token_required

user_router = APIRouter(prefix="/api/users")


@user_router.post("/admin/", status_code=201, response_model=UserResponseSchema)
def create_admin_user(payload: UserAdminCreateSchema, db: Session = Depends(get_db)):
    new_role = Role(name="admin")
    new_tenant = Tenant(name=payload.tenant_name)

    tenant_exists = db.query(Tenant).filter(Tenant.name == new_tenant.name).first()
    if tenant_exists:
        raise HTTPException(401, "Empresa com mesmo nome já existe")

    role_exists = db.query(Role).filter(Role.name == new_role.name).first()
    if role_exists:
        new_role = role_exists

    new_admin = User(
        username=payload.username,
        password=get_password_hash(payload.password),
        role=new_role,
        tenant=new_tenant,
    )
    user_admin_exists = (
        db.query(User).filter(User.username == new_admin.username).first()
    )
    if user_admin_exists:
        raise HTTPException(401, "Usuário com mesmo nome já existe")

    try:
        db.add(new_admin)
        db.add(new_role)
        db.add(new_tenant)
        db.commit()
        db.refresh(new_admin)
        return new_admin
    except Exception:
        db.rollback()
        raise HTTPException(500, "Erro Interno")


@user_router.get(
    "/",
    response_model=List[UserResponseSchema],
    dependencies=[Depends(token_required)],
    status_code=200,
)
def list_users(db: Session = Depends(get_db)) -> List:
    users = db.query(User).all()
    return users


@user_router.get(
    "/{user_id}/",
    response_model=UserResponseSchema,
    dependencies=[Depends(token_required)],
)
def detail_user(user_id: int, db: Session = Depends(get_db)):
    user_exists = db.query(User).filter(User.id == user_id).first()
    if not user_exists:
        raise HTTPException(404, f"Usuário de id '{user_id}' não encontrado")
    return user_exists


@user_router.put(
    "/{user_id}/",
    response_model=UserResponseSchema,
    dependencies=[Depends(token_required)],
)
def update_user_password(
    payload: UserUpdateSchema, user_id: int, db: Session = Depends(get_db)
):
    exc = HTTPException(401, "Credenciais inválidas")

    user_exists = db.query(User).filter(User.id == user_id).first()
    if not user_exists:
        raise exc

    user_is_authenticated = authenticate_user(
        username=user_exists.username, password=payload.password, db=db
    )
    if not user_is_authenticated:
        raise exc

    user_exists.password = get_password_hash(payload.new_password)

    db.commit()
    db.refresh(user_exists)

    return user_exists
