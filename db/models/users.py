from sqlalchemy import Column, String, Integer
from db.config import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), index=True, nullable=False, unique=True)
    password = Column(String(255), nullable=False)
