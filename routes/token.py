from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.config import get_db
from db.models.users import User
from schemas.token import (
    GenerateTokenRequestSchema,
    GenerateTokenResponseSchema,
    VerifyTokenRequestSchema,
)

import jwt
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from utils.security import authenticate_user, validate_token
from utils.const import KEY, ALG, ZONE_INFO, EXP_TIME

token_router = APIRouter(prefix="/api/token")


@token_router.post("/", response_model=GenerateTokenResponseSchema)
def generate_token(payload: GenerateTokenRequestSchema, db: Session = Depends(get_db)):
    login_failed_msg = "usuário e/ou senha incorretos"
    login_credentials = payload.model_dump()

    # 1a verificação: username existe no banco?
    user_exists = (
        db.query(User).filter(User.username == login_credentials["username"]).first()
    )
    if not user_exists:
        raise HTTPException(401, login_failed_msg)

    # 2a verificação: senha fornecida bate com a senha do usuário do banco?
    user_is_authenticated = authenticate_user(
        username=login_credentials["username"],
        password=login_credentials["password"],
        db=db,
    )
    if not user_is_authenticated:
        raise HTTPException(401, login_failed_msg)
    user = user_is_authenticated  # A partir daqui, o usuário existe e é válido

    # Gerar token a partir de um claims definidos
    claims = {}
    claims["exp"] = int(
        (datetime.now(tz=ZoneInfo(ZONE_INFO)) + timedelta(minutes=EXP_TIME)).timestamp()
    )
    claims["user_uuid"] = user.uuid
    token = jwt.encode(payload=claims, key=KEY, algorithm=ALG)

    return {"access": token, "claims": claims}


@token_router.post("/verify/")
def verify_token(payload: VerifyTokenRequestSchema):
    token = payload.model_dump()["token"]
    validate_token(token)
    return {}
