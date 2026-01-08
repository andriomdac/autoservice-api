import uuid
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, func
from db.config import Base


class AutoService(Base):
    __tablename__ = "autoservice"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(
        String(255),
        index=True,
        nullable=False,
        unique=True,
        default=lambda: str(uuid.uuid4()),
    )
    description = Column(String(255), nullable=False)
    service_date = Column(DateTime, nullable=False, index=True)
    service_value = Column(Integer, nullable=False)
    observations = Column(String(255), nullable=True)
    is_paid = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False, default=(func.now))


class PaymentMethod(Base):
    __tablename__ = "payment_method"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(
        String(255),
        index=True,
        nullable=False,
        unique=True,
        default=lambda: str(uuid.uuid4()),
    )
    name = Column(String(20), nullable=False, unique=True)


class PaymentValue(Base):
    __tablename__ = "payment_value"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(
        String(255),
        index=True,
        nullable=False,
        unique=True,
        default=lambda: str(uuid.uuid4()),
    )
    payment_method = Column(Integer, ForeignKey("payment_method.id"), nullable=False)
    autoservice = Column(Integer, ForeignKey("autoservice.id"), nullable=False)
    amount = Column(Integer, nullable=False)
