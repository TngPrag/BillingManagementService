import sys
import types
import pytest
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
# Mock config module
mock_config = types.ModuleType("config")
mock_config.settings = type("Settings", (), {
    "DB_USER": "user",
    "DB_PASSWORD": "pass",
    "DB_HOST": "localhost",
    "DB_PORT": "5432",
    "DB_NAME": "test_db"
})()

sys.modules["config"] = mock_config
sys.modules["config.config"] = mock_config

from fs.fs import (
    fs_create,
    fs_bulk_create,
    fs_read,
    fs_update,
    fs_delete,
    fs_list_many,
    fs_list_all,
    FSResult,
)

Base = declarative_base()

# Simple test User model for testing fs.py
class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)

# Setup a new session fixture with SQLite in-memory
@pytest.fixture(scope="module")
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    session = SessionLocal()
    yield session
    session.close()

def test_fs_create(db_session):
    data = {"full_name": "Alice", "username": "alice1", "email": "alice@example.com"}
    result = fs_create(db_session, User, data)
    assert result.success
    assert result.data.id is not None
    assert result.data.username == "alice1"

def test_fs_bulk_create(db_session):
    users = [
        {"full_name": "Bob", "username": "bob1", "email": "bob@example.com"},
        {"full_name": "Carol", "username": "carol1", "email": "carol@example.com"},
    ]
    result = fs_bulk_create(db_session, User, users)
    assert result.success
    assert len(result.data) == 2

def test_fs_read(db_session):
    # Assuming user with id=1 exists from previous test
    result = fs_read(db_session, User, 1)
    assert result.success
    assert result.data.username == "alice1"

def test_fs_update(db_session):
    result_read = fs_read(db_session, User, 1)
    user_obj = result_read.data
    updates = {"full_name": "Alice Updated"}
    result = fs_update(db_session, user_obj, updates)
    assert result.success
    assert result.data.full_name == "Alice Updated"

def test_fs_delete(db_session):
    # Delete user with id=2 (Bob)
    result = fs_delete(db_session, User, 2)
    assert result.success

    # Confirm deleted
    result_check = fs_read(db_session, User, 2)
    assert not result_check.success
    assert result_check.error == "Object not found"

def test_fs_list_many(db_session):
    filters = {"username": "carol1"}
    result = fs_list_many(db_session, User, filters)
    # Carol was deleted in bulk_create, but not in delete test, so should be there
    assert result.success
    for user in result.data:
        assert user.username == "carol1"

def test_fs_list_all(db_session):
    result = fs_list_all(db_session, User)
    assert result.success
    assert len(result.data) >= 1  # At least Alice and Carol or Alice only after deletes
