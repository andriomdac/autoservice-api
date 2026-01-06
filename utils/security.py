from fastapi.requests import Request
from pwdlib import PasswordHash
from db.models.users import User
from sqlalchemy.orm import Session
import jwt
from jwt.exceptions import DecodeError, ExpiredSignatureError
from fastapi.exceptions import HTTPException
from utils.const import key, alg

pwd_context = PasswordHash.recommended()


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hash: str) -> bool:
    return pwd_context.verify(password, hash)


def authenticate_user(username: str, password: str, db: Session) -> User | None:
    """
    Verifica as credenciais de um usuário no banco de dados.

    Busca um usuário pelo nome de usuário fornecido e valida a senha
    comparando o texto puro com o hash armazenado.

    Args:
        username (str): O nome de usuário para busca.
        password (str): A senha em texto puro para verificação.
        db (Session): A instância da sessão do banco de dados SQLAlchemy.

    Returns:
        User: O objeto do usuário se a autenticação for bem-sucedida.
        None: Se o usuário não for encontrado ou a senha estiver incorreta.
    """
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return None
    if verify_password(password=password, hash=str(user.password)):
        return user
    else:
        return None


def validate_token(token: str) -> None:
    """
    Valida a integridade e a expiração de um token JWT.

    Decodifica o token usando a chave e o algoritmo pré-definidos. Caso o token
    esteja malformado, com assinatura inválida ou expirado, uma exceção HTTP 401
    é lançada.

    Args:
        token (str): O token JWT a ser validado.

    Raises:
        HTTPException: Se o token for inválido (DecodeError) ou se o tempo
            de expiração tiver passado (ExpiredSignatureError).

    Returns:
        None: Se o token for válido e a decodificação ocorrer sem erros.
    """
    fail_msg = "token inválido ou expirado"
    try:
        jwt.decode(jwt=token, key=key, algorithms=[alg])
        pass
    except DecodeError:
        raise HTTPException(401, fail_msg)
    except ExpiredSignatureError:
        raise HTTPException(401, fail_msg)


def token_required(request: Request) -> None:
    headers = request.headers
    token = headers.get("authorization")
    if token:
        token = token.split(sep=" ")[1]
    else:
        token = ""
    validate_token(token)
