import uuid
from datetime import datetime
from typing import List
from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Session

from fs.fs import (
    Base,
    fs_create,
    fs_read,
    fs_update,
    fs_delete,
    fs_list_all,
    fs_list_many,
    FSResult
)

# -------------------
# SQLAlchemy ORM model
# -------------------
class Bill(Base):
    __tablename__ = "bills"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)
    biller_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False)
    due_date = Column(DateTime, nullable=False)
    status = Column(String, default="pending")  # pending, paid, overdue
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# -------------------
# Core CRUD logic
# -------------------
def create_bill(db: Session, data: dict) -> FSResult[Bill]:
    return fs_create(db, Bill, data)

def get_bill_by_id(db: Session, bill_id: uuid.UUID) -> FSResult[Bill]:
    return fs_read(db, Bill, bill_id)

def get_bills_by_customer_id(db: Session, customer_id: uuid.UUID) -> FSResult[List[Bill]]:
    result = fs_list_many(db, Bill, {"customer_id": customer_id})
    if result.success and result.data:
        return FSResult(success=True, data=result.data)
    return FSResult(success=False, error="Bills for customer not found")

def get_bills_by_biller_id(db: Session, biller_id: uuid.UUID) -> FSResult[List[Bill]]:
    result = fs_list_many(db, Bill, {"biller_id": biller_id})
    if result.success and result.data:
        return FSResult(success=True, data=result.data)
    return FSResult(success=False, error="Bills for biller not found")

def update_bill(db: Session, bill_id: uuid.UUID, updates: dict) -> FSResult[Bill]:
    read_result = get_bill_by_id(db, bill_id)
    if not read_result.success:
        return FSResult(success=False, error=read_result.error)

    return fs_update(db, read_result.data, updates)

def delete_bill(db: Session, bill_id: uuid.UUID) -> FSResult[None]:
    return fs_delete(db, Bill, bill_id)

def list_many_bills_by_status(db: Session, status: str) -> FSResult[List[Bill]]:
    result = fs_list_many(db, Bill, {"status": status})
    if result.success and result.data:
        return FSResult(success=True, data=result.data)
    return FSResult(success=False, error=f"No bills with status '{status}' found")

def list_bills(db: Session) -> FSResult[List[Bill]]:
    return fs_list_all(db, Bill)
