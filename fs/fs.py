# fs/fs.py
"""
Why fs.py?
==========
Separation of concerns: It separates DB logic and exceptions cleanly.

Clean result contracts: Handlers can directly check .success and handle .error.

Logging for monitoring: Errors are logged with operation context.

Typed and generic-friendly: Makes use of TypeVar, Generic[T], and BaseModel.

Safe rollback behavior: In all cases of failure.
"""
import logging
import uuid
from typing import Any, Type, List, Optional, TypeVar, Generic

from sqlalchemy import create_engine
from sqlalchemy.orm import as_declarative
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.ext.declarative import declared_attr
from pydantic import BaseModel
from sqlalchemy import MetaData
from config.config import settings

# =========================
# Logging Setup
# =========================
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# =========================
# SQLAlchemy Base
# =========================
@as_declarative()
class Base:
    id: Any
    __name__: str
    metadata: MetaData = MetaData()
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

# =========================
# Database Configuration
# =========================
# =========================
# Database Configuration
# =========================
DATABASE_URL = "sqlite:///./billingmanager.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

#Base.metadata.create_all(bind=engine)  # Optional: ensure tables are created
"""
DATABASE_URL = (
    f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}"
    f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
)

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
"""
# Open session
def fs_open() -> Session:
    return SessionLocal()

# =========================
# Result Schema
# =========================
T = TypeVar("T")

class FSResult(BaseModel, Generic[T]):
    success: bool
    data: Optional[T] = None
    error: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True

# =========================
# Custom Exceptions (optional for handler use)
# =========================
class CRUDException(Exception):
    pass

class ObjectNotFound(CRUDException):
    def __init__(self, model_name: str, obj_id: Any):
        super().__init__(f"{model_name} with ID {obj_id} not found")

class DuplicateEntry(CRUDException):
    def __init__(self, message: str = "Duplicate entry"):
        super().__init__(message)

class DatabaseError(CRUDException):
    def __init__(self, message: str = "Database error"):
        super().__init__(message)
#Create tables
def create_tables():
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully.")
    except Exception as e:
        logger.error(f"Error creating tables: {e}")
        raise

# =========================
# CRUD Functions
# =========================


def fs_create(db: Session, model: Type[Base], data: dict) -> FSResult:
    """
    Create a new record for the given SQLAlchemy model.
    """
    try:
        obj = model(**data)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return FSResult(success=True, data=obj)
    except TypeError as e:
        logger.error(f"[fs_create] TypeError: Invalid field in data: {e}")
        return FSResult(success=False, error=f"Invalid input: {e}")
    except IntegrityError as e:
        db.rollback()
        logger.error(f"[fs_create] IntegrityError: {e}")
        return FSResult(success=False, error="Duplicate entry")
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"[fs_create] SQLAlchemyError: {e}")
        return FSResult(success=False, error="Database error")

def fs_bulk_create(db: Session, model: Type[Base], data_list: List[dict]) -> FSResult:
    """
    Bulk insert many records.
    """
    try:
        objects = [model(**data) for data in data_list]
        db.bulk_save_objects(objects)
        db.commit()
        return FSResult(success=True, data=objects)
    except (TypeError, IntegrityError, SQLAlchemyError) as e:
        db.rollback()
        logger.error(f"[fs_bulk_create] Error: {e}")
        return FSResult(success=False, error="Database error during bulk insert")

def fs_read(db: Session, model: Type[Base], obj_id: Any) -> FSResult:
    """
    Read an object by ID.
    """
    try:
        obj = db.query(model).filter(model.id == obj_id).first()
        if obj:
            return FSResult(success=True, data=obj)
        return FSResult(success=False, error="Object not found")
    except SQLAlchemyError as e:
        logger.error(f"[fs_read] SQLAlchemyError: {e}")
        return FSResult(success=False, error="Database error")



def fs_update(db: Session, obj: Base, updates: dict) -> FSResult:
    """
    Update an existing object with provided updates.
    """
    try:
        for field, value in updates.items():
            if hasattr(obj, field):
                setattr(obj, field, value)
        db.commit()
        db.refresh(obj)
        return FSResult(success=True, data=obj)
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"[fs_update] SQLAlchemyError: {e}")
        return FSResult(success=False, error="Database error during update")


def fs_delete(db: Session, model: Type[Base], obj_id: Any) -> FSResult:
    """
    Delete an object by ID.
    """
    try:
        obj = db.query(model).filter(model.id == obj_id).first()
        if not obj:
            return FSResult(success=False, error="Object not found")
        db.delete(obj)
        db.commit()
        return FSResult(success=True)
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"[fs_delete] SQLAlchemyError: {e}")
        return FSResult(success=False, error="Database error during delete")


def fs_list_many(db: Session, model: Type[Base], filters: dict) -> FSResult:
    """
    List multiple objects that match the provided filters.

    Args:
        db: SQLAlchemy session.
        model: SQLAlchemy model class.
        filters: Dictionary of filters to apply to the query.

    Returns:
        FSResult with a list of matching objects or an error.
    """
    try:
        query = db.query(model)
        for attr, value in filters.items():
            if hasattr(model, attr):
                query = query.filter(getattr(model, attr) == value)
            else:
                logger.warning(f"[fs_list_many] Ignored unknown filter field: {attr}")
        items = query.all()
        return FSResult(success=True, data=items)
    except SQLAlchemyError as e:
        logger.error(f"[fs_list_many] SQLAlchemyError: {e}")
        return FSResult(success=False, error="Database error during filtered list")


def fs_list_all(db: Session, model: Type[Base]) -> FSResult:
    try:
        items = db.query(model).all()
        return FSResult(success=True, data=items)
    except SQLAlchemyError as e:
        logger.error(f"[fs_list] SQLAlchemyError: {e}")
        return FSResult(success=False, error="Database error during list")
