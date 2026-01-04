from pwdlib import PasswordHash
from db.models.users import User
from sqlalchemy.orm import Session

pwd_context = PasswordHash.recommended()


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hash: str) -> bool:
    return pwd_context.verify(password, hash)


def authenticate_user(username: str, password: str, db: Session):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return None
    if verify_password(password=password, hash=user.password):
        return user
    else:
        return None
