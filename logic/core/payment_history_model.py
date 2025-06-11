import uuid
from datetime import datetime
from typing import List
from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Session

from fs.fs import Base, fs_create, fs_read, fs_update, fs_delete, fs_list_all, fs_list_many, FSResult

# -------------------
# SQLAlchemy ORM model
# -------------------
class Payment(Base):
    __tablename__ = "payments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)
    bill_id = Column(UUID(as_uuid=True), ForeignKey("bills.id"), nullable=False)
    biller_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False)
    paid_on = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# -------------------
# Core CRUD logic
# -------------------


def create_payment(db: Session,data: dict) -> FSResult[Payment]:
    return fs_create(db,Payment,data)
#Enables to read payment by bill id
def read_payment_by_id(db: Session,bill_id: uuid.UUID) -> FSResult[Payment]:
    return fs_read(db,Payment,bill_id)
# Enables to read payments done by customer_id
def read_payments_by_customer_id(db: Session,customer_id:uuid.UUID) -> FSResult[list[Payment]]:
    return fs_list_many(db,Payment,{"customer_id":customer_id})
#Enables to read payments done by biller_id
def read_payments_by_biller_id(db: Session,biller_id:uuid.UUID) -> FSResult[list[Payment]]:
    return fs_list_many(db,Payment,{"customer_id":biller_id})
#list all payments
def list_payments(db: Session)-> FSResult[list[Payment]]:
    return fs_list_all(db,Payment)

