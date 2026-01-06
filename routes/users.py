from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.users import UserCreateSchema, UserList, UserResponseSchema
from db.models.users import User
from db.config import get_db
from utils.security import get_password_hash, token_required

user_router = APIRouter(prefix="/api/users")


@user_router.post("/", dependencies=[Depends(token_required)], status_code=201)
def create_user(
    payload: UserCreateSchema,
    db: Session = Depends(get_db),
):
    body = payload.model_dump()
    username = body["username"]
    password = body["password"]

    new_user = User(username=username, password=get_password_hash(password))

    user_exists = db.query(User).filter(User.username == username).first()
    if user_exists:
        raise HTTPException(409, f"Usuário {username} já existe")

    else:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return UserResponseSchema(
            username=str(new_user.username), uuid=str(new_user.uuid)
        )


@user_router.get(
    "/",
    response_model=List[UserList],
    dependencies=[Depends(token_required)],
    status_code=200,
)
def list_users(db: Session = Depends(get_db)) -> List:
    users = db.query(User).all()
    return users
