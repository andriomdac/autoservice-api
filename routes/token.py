from re import error
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from schemas.token import VerifyTokenSchema, LoginSchema
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from db.config import get_db
from zoneinfo import ZoneInfo
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError, DecodeError
from utils.security import authenticate_user
from utils.messages import error_message


token_router = APIRouter(prefix="/api/token")

# Todas essas infos abaixo devem ser variáveis de ambiente
secret_key = "fklu342kfnmvzfjgu321fjdnvcxzçdsu221rdnvb88321nvwdiog89u4304t"
alg = "HS256"
tz_info = "America/Sao_Paulo"
expiration_time = 30


@token_router.post("/")
def get_token(payload: LoginSchema, db: Session = Depends(get_db)):
    user = payload.model_dump()
    claims = {}
    user_exists = authenticate_user(
        username=user["username"], password=user["password"], db=db
    )
    if user_exists:
        claims["user_uuid"] = str(user_exists.uuid)
        claims["exp"] = int(
            (
                datetime.now(ZoneInfo(tz_info)) + timedelta(minutes=expiration_time)
            ).timestamp()
        )
        token = jwt.encode(payload=claims, key=secret_key, algorithm=alg)
        return JSONResponse({"access": token}, status_code=200)
    else:
        return error_message("Usuário ou senha incorretos")


@token_router.post("/verify/")
def verify_token(payload: VerifyTokenSchema):
    token = payload.model_dump()["token"]
    try:
        decoded = jwt.decode(jwt=token, key=secret_key, algorithms=[alg])
        return decoded
    except DecodeError:
        return error_message("token inválido", 400)
    except ExpiredSignatureError:
        return error_message("token expirado", 401)
