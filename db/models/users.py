from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from db.config import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(
        String(255), index=True, unique=True, nullable=False
    )
    role_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("roles.id"), nullable=False
    )
    tenant_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("tenants.id"), nullable=False
    )
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    # relacionamentos
    tenant = relationship("Tenant", back_populates="users")
    role = relationship("Role", back_populates="users")


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    # relacionamentos
    users = relationship("User", back_populates="role")
