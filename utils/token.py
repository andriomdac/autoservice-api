import jwt
from jwt.exceptions import ExpiredSignatureError, DecodeError
from datetime import timedelta, datetime, timezone

from utils.exceptions import CustomErrorException


EXP_TIME = timedelta(minutes=5)
SECRET = "e501d4631423a04885812852b5996a0b074ef599333e26a148b3167c5ff6a05e"
ALGORITHM = "HS256"


def generate_token() -> str:
    claims = {"exp": datetime.now(timezone.utc) + EXP_TIME}
    encoded = jwt.encode(claims, SECRET, ALGORITHM)
    return encoded


def decode_token(token: str, return_decoded: bool = False) -> dict:
    try:
        decoded = jwt.decode(jwt=token, key=SECRET, algorithms=[ALGORITHM])
        if return_decoded:
            return decoded
    except ExpiredSignatureError:
        raise CustomErrorException("Token expirado")
    except (DecodeError,):
        raise CustomErrorException("Token inválido")
    return {}
