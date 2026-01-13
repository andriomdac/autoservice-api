from datetime import datetime
from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.config import Base


class Tenant(Base):
    __tablename__ = "tenants"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(
        String(255), nullable=False, index=True, unique=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    # relacionamentos
    users = relationship("User", back_populates="tenant")
