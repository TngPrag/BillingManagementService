import uuid
import pytest
from datetime import datetime, timedelta

from logic.core.bill_model import  (
    create_bill, get_bill_by_id, get_bills_by_customer_id, get_bills_by_biller_id,
    update_bill, delete_bill, list_bills
)
from fs.fs import FSResult

# You need a fixture that provides a fresh DB session for testing.
# This depends on your setup, but here is a generic placeholder:
@pytest.fixture
def db_session():
    # Setup your test DB session (e.g., with SQLAlchemy's sessionmaker, SQLite in-memory, or test DB)
    from fs.fs import SessionLocal  # example import, adjust to your project
    session = SessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()

def create_sample_bill_dict(biller_id=None, customer_id=None):
    return {
        "biller_id": biller_id or uuid.uuid4(),
        "customer_id": customer_id or uuid.uuid4(),
        "amount": 150.75,
        "due_date": datetime.utcnow() + timedelta(days=30),
        "status": "pending",
        "description": "Electricity bill for May",
    }

def test_create_and_get_bill(db_session):
    bill_data = create_sample_bill_dict()
    result: FSResult = create_bill(db_session, bill_data)
    assert result.success
    bill = result.data
    assert bill.id is not None
    assert bill.amount == bill_data["amount"]

    # Get the bill by id
    get_result = get_bill_by_id(db_session, bill.id)
    assert get_result.success
    assert get_result.data.id == bill.id

def test_list_bills_by_customer_and_biller(db_session):
    # Create two bills for the same customer and biller
    customer_id = uuid.uuid4()
    biller_id = uuid.uuid4()
    bill1 = create_bill(db_session, create_sample_bill_dict(biller_id, customer_id)).data
    bill2 = create_bill(db_session, create_sample_bill_dict(biller_id, customer_id)).data

    # List by customer_id
    customer_bills_result = get_bills_by_customer_id(db_session, customer_id)
    assert customer_bills_result.success
    assert len(customer_bills_result.data) >= 2
    assert all(b.customer_id == customer_id for b in customer_bills_result.data)

    # List by biller_id
    biller_bills_result = get_bills_by_biller_id(db_session, biller_id)
    assert biller_bills_result.success
    assert len(biller_bills_result.data) >= 2
    assert all(b.biller_id == biller_id for b in biller_bills_result.data)

def test_update_bill(db_session):
    bill_data = create_sample_bill_dict()
    created = create_bill(db_session, bill_data).data

    update_data = {"status": "paid", "description": "Paid in full"}
    update_result = update_bill(db_session, created.id, update_data)
    assert update_result.success
    updated_bill = update_result.data
    assert updated_bill.status == "paid"
    assert updated_bill.description == "Paid in full"

def test_delete_bill(db_session):
    bill_data = create_sample_bill_dict()
    created = create_bill(db_session, bill_data).data

    delete_result = delete_bill(db_session, created.id)
    assert delete_result.success

    # Confirm deletion
    get_result = get_bill_by_id(db_session, created.id)
    assert not get_result.success

def test_list_all_bills(db_session):
    # Create a couple of bills
    create_bill(db_session, create_sample_bill_dict())
    create_bill(db_session, create_sample_bill_dict())

    list_result = list_bills(db_session)
    assert list_result.success
    assert len(list_result.data) >= 2
