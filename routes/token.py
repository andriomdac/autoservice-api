from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from db.config import get_db
from schemas.token import LoginSchema, VerifyTokenSchema
from utils.exceptions import CustomErrorException
from utils.messages import success_message, error_message
from db.models.users import User
from utils.security import verify_password
from utils.token import decode_token, generate_token
from icecream import ic

token_router = APIRouter(prefix="/api/token")


@token_router.post("/")
def get_token(payload: LoginSchema, db: Session = Depends(get_db)):
    data = payload.model_dump()

    user = db.query(User).filter(User.username == data["username"]).first()
    if not user:
        return error_message("Usuário não encontrado", 404)
    if not verify_password(password=data["password"], hash=f"{user.password}"):
        return error_message("Senha inválida")

    generated_token = generate_token()

    return JSONResponse({"access": generated_token}, status_code=201)


@token_router.post("/verify/")
def verify_token(payload: VerifyTokenSchema):
    token = payload.model_dump()["token"]
    ic(token)
    try:
        decode_token(token)
    except CustomErrorException as e:
        return error_message(f"{e}", 400)
    return JSONResponse(None)
