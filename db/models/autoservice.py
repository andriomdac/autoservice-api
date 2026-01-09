from datetime import datetime
import uuid
from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
)
from zoneinfo import ZoneInfo
from utils.const import ZONE_INFO
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
    service_date = Column(Date, nullable=False, index=True)
    service_value = Column(Integer, nullable=False)
    observations = Column(String(255), nullable=True)
    is_paid = Column(Boolean, nullable=False, default=False)
    created_at = Column(
        DateTime,
        nullable=False,
        default=(lambda: datetime.now(ZoneInfo(ZONE_INFO))),
    )


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
    payment_method = Column(
        String(255), ForeignKey("payment_method.uuid"), nullable=False
    )
    autoservice = Column(String(255), ForeignKey("autoservice.uuid"), nullable=False)
    amount = Column(Integer, nullable=False)
