from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID
from datetime import datetime


# Shared DTO for Monthly Aggregation
class MonthlyReportDto(BaseModel):
    month: str  # e.g., "2025-05"
    bills_created: Optional[int] = 0
    amount_billed: float
    amount_paid: float
    amount_outstanding: Optional[float] = 0.0
    new_billers: Optional[int] = 0
    new_customers: Optional[int] = 0


# ---------- Admin DTOs ----------

class AdminTopBillerDto(BaseModel):
    biller_id: UUID
    biller_name: str
    bills_issued: int
    amount_billed: float
    paid_ratio: float


class AdminTopDebtorDto(BaseModel):
    customer_id: UUID
    customer_name: str
    outstanding_amount: float
    overdue_bills: int


class AdminReportDto(BaseModel):
    total_billers: int
    total_customers: int
    total_bills_systemwide: int
    total_amount_billed: float
    total_paid_amount: float
    total_outstanding_amount: float
    monthly_report: List[MonthlyReportDto]
    top_billers: List[AdminTopBillerDto]
    top_debtors: List[AdminTopDebtorDto]


# ---------- Biller DTOs ----------

class BillerCustomerBillSummaryDto(BaseModel):
    customer_id: UUID
    customer_name: str
    total_bills: int
    paid: int
    pending: int
    overdue: int
    total_billed: float
    total_paid: float


class BillerReportDto(BaseModel):
    total_bills_issued: int
    total_amount_billed: float
    total_paid_amount: float
    total_outstanding_amount: float
    paid_bills_count: int
    pending_bills_count: int
    overdue_bills_count: int
    bills_per_customer: List[BillerCustomerBillSummaryDto]
    monthly_aggregation: List[MonthlyReportDto]


# ---------- Customer DTOs ----------

class CustomerBillByBillerDto(BaseModel):
    biller_id: UUID
    biller_name: str
    total_billed: float
    total_paid: float
    outstanding: float


class PaymentHistoryDto(BaseModel):
    bill_id: UUID
    amount: float
    paid_on: datetime
    status: str


class CustomerReportDto(BaseModel):
    total_bills_received: int
    total_amount_due: float
    total_paid: float
    outstanding_amount: float
    paid_bills: int
    pending_bills: int
    overdue_bills: int
    bills_by_biller: List[CustomerBillByBillerDto]
    payment_history: List[PaymentHistoryDto]
