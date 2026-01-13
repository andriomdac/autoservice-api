from datetime import date, datetime
from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.config import Base


class AutoService(Base):
    __tablename__ = "autoservices"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    description: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    service_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    tenant_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("tenants.id"), nullable=False
    )
    service_value: Mapped[int] = mapped_column(Integer, nullable=False)
    observations: Mapped[str] = mapped_column(String(255), nullable=False)
    is_paid: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    # Relacionamentos
    payment_values = relationship(
        "PaymentValue", back_populates="autoservice", cascade="all, delete-orphan"
    )
    tenant = relationship("Tenant", back_populates="autoservices")


class PaymentMethod(Base):
    __tablename__ = "payment_methods"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), index=True, nullable=False)

    # Relacionamentos
    payment_values = relationship("PaymentValue", back_populates="payment_method")


class PaymentValue(Base):
    __tablename__ = "payment_values"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    payment_method_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("payment_methods.id", ondelete="RESTRICT"), nullable=False
    )
    autoservice_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("autoservices.id", ondelete="CASCADE"), nullable=False
    )
    amount: Mapped[int] = mapped_column(Integer, nullable=False)

    # Relacionamentos
    autoservice = relationship("AutoService", back_populates="payment_values")
    payment_method = relationship("PaymentMethod", back_populates="payment_values")
