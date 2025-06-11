import uuid
from typing import List
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional
from fs.fs import Base, fs_create, fs_read, fs_update, fs_delete, fs_list_all,fs_list_many, FSResult
from sqlalchemy import Column, String, DateTime, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID

from logic.core.security import hash_password

# -------------------
# SQLAlchemy ORM model
# -------------------
class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)
    full_name = Column(String, nullable=False)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False, default="customer")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint('username', name='uq_username'),
        UniqueConstraint('email', name='uq_email'),
    )


# -------------------
# Core CRUD logic
# -------------------
def create_user(db: Session, user_data: dict) -> FSResult[User]:

    return fs_create(db, User, user_data)


def get_user_by_id(db: Session, user_id: uuid.UUID) -> FSResult[User]:
    return fs_read(db, User, user_id)

def get_users_by_role(db: Session, role: str) -> FSResult[List[User]]:
    result = fs_list_many(db, User, {"role": role})
    if result.success and result.data:
        return FSResult(success=True, data=result.data)
    return FSResult(success=False, error="Users not found")
def get_user_by_username(db: Session, username: str) -> FSResult[User]:
    result = fs_list_many(db, User, {"username": username})
    #print(result)
    if result.success and result.data:
        return FSResult(success=True, data=result.data[0])
    return FSResult(success=False, error="User not found")

def update_user(db: Session, user_id: uuid.UUID, updates: dict) -> FSResult[User]:
    read_result = fs_read(db, User, user_id)
    if not read_result.success:
        return FSResult(success=False, error=read_result.error)

    return fs_update(db, read_result.data, updates)

def delete_user(db: Session, user_id: uuid.UUID) -> FSResult[None]:
    return fs_delete(db, User, user_id)


def list_users(db: Session) -> FSResult[List[User]]:
    return fs_list_all(db, User)


# -------------------
# Initialize default admin
# -------------------
def init_admin_user(db: Session):
    from sqlalchemy import select


    existing_admin = db.execute(
        select(User).where(User.role == "admin")
    ).scalar_one_or_none()

    if not existing_admin:
        admin_data = {
            "full_name": "System Admin",
            "username": "admin",
            "email": "admin@example.com",
            "password_hash": hash_password("Password123!"),
            "role": "admin"
        }

        return create_user(db, admin_data)
