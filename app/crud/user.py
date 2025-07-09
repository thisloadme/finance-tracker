from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password
from typing import Optional

def get_user(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(
        and_(User.user_id == user_id, User.deleted_at.is_(None))
    ).first()

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(
        and_(User.email == email, User.deleted_at.is_(None))
    ).first()

def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(
        and_(User.username == username, User.deleted_at.is_(None))
    ).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).filter(User.deleted_at.is_(None)).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate) -> User:
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password,
        full_name=user.full_name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user_update: UserUpdate) -> Optional[User]:
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    
    update_data = user_update.dict(exclude_unset=True)
    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
    
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int) -> bool:
    db_user = get_user(db, user_id)
    if not db_user:
        return False
    
    # Soft delete
    from datetime import datetime
    db_user.deleted_at = datetime.utcnow()
    db.commit()
    return True

def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user 