import uuid
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from logic.core.user_model import (
    Base, User, create_user, get_user_by_id, update_user,
    delete_user, list_users, init_admin_user
)
from logic.core.security import hash_password

# --- Setup in-memory SQLite test DB ---
TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --- Fixture for DB session ---
@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)

# --- Sample user data ---
def sample_user_data():
    return {
        "full_name": "John Doe",
        "username": "johndoe",
        "email": "john@example.com",
        "password_hash": hash_password("secret123"),
        "role": "customer"
    }

# --- Tests ---
def test_create_user(db):
    result = create_user(db, sample_user_data())
    assert result.success
    assert result.data.username == "johndoe"

def test_get_user_by_id(db):
    create_result = create_user(db, sample_user_data())
    user_id = create_result.data.id

    get_result = get_user_by_id(db, user_id)
    assert get_result.success
    assert get_result.data.email == "john@example.com"

def test_update_user(db):
    create_result = create_user(db, sample_user_data())
    user_id = create_result.data.id

    updates = {"full_name": "Jane Doe"}
    update_result = update_user(db, user_id, updates)

    assert update_result.success
    assert update_result.data.full_name == "Jane Doe"

def test_delete_user(db):
    create_result = create_user(db, sample_user_data())
    user_id = create_result.data.id

    delete_result = delete_user(db, user_id)
    assert delete_result.success

    get_result = get_user_by_id(db, user_id)
    assert not get_result.success

def test_list_users(db):
    create_user(db, sample_user_data())
    create_user(db, {
        "full_name": "Alice Smith",
        "username": "alice",
        "email": "alice@example.com",
        "password_hash": hash_password("secret123"),
        "role": "customer"
    })

    result = list_users(db)
    assert result.success
    assert len(result.data) == 2

def test_init_admin_user(db):
    result = init_admin_user(db)
    assert result.success
    assert result.data.role == "admin"
    assert result.data.username == "admin"
