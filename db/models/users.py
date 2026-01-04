from sqlalchemy import Column, String, Integer
import uuid
from db.config import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(
        String(255),
        index=True,
        nullable=False,
        unique=True,
        default=lambda: str(uuid.uuid4()),
    )
    username = Column(String(255), index=True, nullable=False, unique=True)
    password = Column(String(255), nullable=False)
