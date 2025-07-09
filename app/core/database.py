from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from contextlib import contextmanager
from app.config import settings
import logging

logger = logging.getLogger(__name__)

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    pool_size=10,
    max_overflow=20
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        logger.error(f"Database error: {e}")
        db.rollback()
        raise
    finally:
        db.close()

@contextmanager
def get_db_transaction():
    """Context manager for database transactions with automatic rollback on error"""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        logger.error(f"Transaction failed: {e}")
        raise
    finally:
        db.close()

def execute_with_retry(func, max_retries=3):
    """Execute function with retry logic for concurrent operations"""
    for attempt in range(max_retries):
        try:
            return func()
        except IntegrityError as e:
            if attempt == max_retries - 1:
                raise
            logger.warning(f"Retry attempt {attempt + 1} due to integrity error: {e}")
            continue 