# logic/DTO/bill_dto.py

import uuid
from enum import Enum
from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field


class BillStatus(str, Enum):
    """Enum representing valid statuses for a bill."""
    pending = "pending"
    paid = "paid"
    overdue = "overdue"


class CreateBillDto(BaseModel):
    """
    DTO for creating a bill.
    """
    biller_id: uuid.UUID = Field(..., description="ID of the biller")
    customer_id: uuid.UUID = Field(..., description="ID of the customer")
    amount: float = Field(..., gt=0, description="Amount of the bill")
    status: BillStatus = Field(..., description="Status of the bill")
    description: Optional[str] = Field(None, description="Description of the bill")
    due_date: Optional[datetime] = Field(None, description="Due date of the bill in ISO format")


class UpdateBillDto(BaseModel):
    """
    DTO for updating a bill.
    """
    customer_id: Optional[uuid.UUID] = Field(None, description="ID of the customer")
    amount: Optional[float] = Field(None, gt=0, description="Amount of the bill")
    status: Optional[BillStatus] = Field(None, description="Status of the bill")
    description: Optional[str] = Field(None, description="Description of the bill")
    due_date: Optional[datetime] = Field(None, description="Due date of the bill in ISO format")


class BillResponseDto(BaseModel):
    """
    DTO for returning bill information to clients.
    """
    id: int
    customer_id: uuid.UUID
    amount: float
    status: BillStatus
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
