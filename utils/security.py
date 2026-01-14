from typing import Optional
from fastapi import Depends
from fastapi.requests import Request
from pwdlib import PasswordHash
from db.config import get_db
from db.models.users import User
from sqlalchemy.orm import Session
import jwt
from jwt.exceptions import DecodeError, ExpiredSignatureError
from fastapi.exceptions import HTTPException
from utils.const import KEY, ALG

pwd_context = PasswordHash.recommended()


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hash: str) -> bool:
    return pwd_context.verify(password, hash)


def authenticate_user(username: str, password: str, db: Session) -> User | None:
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return None
    if verify_password(password=password, hash=str(user.password)):
        return user
    else:
        return None


def validate_token(token: str) -> dict:
    fail_msg = "token inválido ou expirado"
    try:
        return jwt.decode(jwt=token, key=KEY, algorithms=[ALG])
    except (DecodeError, ExpiredSignatureError):
        raise HTTPException(401, fail_msg)


def get_token_from_header(request: Request):
    headers = request.headers
    token = headers.get("authorization")

    if token:
        token = token.split(sep=" ")[1]
    else:
        token = ""

    return token


def get_current_user(request: Request, db: Session = Depends(get_db)) -> User:
    fail_msg = "token inválido ou expirado"
    token = get_token_from_header(request=request)
    user_id = validate_token(token=token)["sub"]
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(401, fail_msg)
    return user


def token_required(request: Request) -> None:
    token = get_token_from_header(request)
    validate_token(token)
