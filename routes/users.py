from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.users import UserCreateSchema
from db.models.users import User
from db.config import get_db
from utils.messages import error_message, success_message


user_router = APIRouter(prefix="/api/users")


@user_router.post("/")
def create_user(payload: UserCreateSchema, db: Session = Depends(get_db)):
    body = payload.model_dump()
    username = body["username"]
    password = body["password"]

    new_user = User(username=username, password=password)
    user_exists = db.query(User).filter(User.username == username).first()
    if user_exists:
        return error_message("Este nome de usuário já existe", 409)
    else:
        db.add(new_user)
        db.commit()
        return success_message(f"Usuário {username} criado", 201)
