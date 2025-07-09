from sqlalchemy.orm import Session
from sqlalchemy import func, or_, and_
from app.models.transaction import Transaction, TransactionType
from app.models.budget import BudgetCategory
from app.schemas.transaction import TransactionCreate, TransactionUpdate
from typing import List, Optional
from datetime import datetime, date
from decimal import Decimal
from app.core.database import execute_with_retry
import logging

logger = logging.getLogger(__name__)

def get_transaction(db: Session, transaction_id: int, user_id: int) -> Optional[Transaction]:
    return db.query(Transaction).filter(
        and_(Transaction.transaction_id == transaction_id, Transaction.user_id == user_id)
    ).first()

def get_transactions(
    db: Session, 
    user_id: int, 
    skip: int = 0, 
    limit: int = 100,
    category_id: Optional[int] = None,
    transaction_type: Optional[TransactionType] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    search: Optional[str] = None
) -> List[Transaction]:
    query = db.query(Transaction).filter(Transaction.user_id == user_id)
    
    if category_id:
        query = query.filter(Transaction.category_id == category_id)
    
    if transaction_type:
        query = query.filter(Transaction.type == transaction_type)
    
    if start_date:
        query = query.filter(Transaction.date >= start_date)
    
    if end_date:
        query = query.filter(Transaction.date <= end_date)
    
    if search:
        query = query.filter(
            Transaction.description.ilike(f"%{search}%")
        )
    
    return query.order_by(Transaction.date.desc()).offset(skip).limit(limit).all()

def validate_category_exists(db: Session, category_id: int, user_id: int) -> bool:
    """Validate that category exists and belongs to user"""
    if category_id is None:
        return True
    
    category = db.query(BudgetCategory).filter(
        and_(BudgetCategory.category_id == category_id, BudgetCategory.user_id == user_id)
    ).first()
    
    return category is not None

def create_transaction(db: Session, transaction: TransactionCreate, user_id: int) -> Transaction:
    # Validate category exists
    if not validate_category_exists(db, transaction.category_id, user_id):
        raise ValueError("Category does not exist or does not belong to user")
    
    def _create():
        db_transaction = Transaction(
            user_id=user_id,
            category_id=transaction.category_id,
            type=transaction.type,
            amount=transaction.amount,
            description=transaction.description,
            date=transaction.date
        )
        db.add(db_transaction)
        db.commit()
        db.refresh(db_transaction)
        return db_transaction
    
    return execute_with_retry(_create)

def update_transaction(db: Session, transaction_id: int, user_id: int, transaction_update: TransactionUpdate) -> Optional[Transaction]:
    db_transaction = get_transaction(db, transaction_id, user_id)
    if not db_transaction:
        return None
    
    # Validate category exists if updating
    if transaction_update.category_id is not None:
        if not validate_category_exists(db, transaction_update.category_id, user_id):
            raise ValueError("Category does not exist or does not belong to user")
    
    def _update():
        update_data = transaction_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_transaction, field, value)
        
        db.commit()
        db.refresh(db_transaction)
        return db_transaction
    
    return execute_with_retry(_update)

def delete_transaction(db: Session, transaction_id: int, user_id: int) -> bool:
    db_transaction = get_transaction(db, transaction_id, user_id)
    if not db_transaction:
        return False
    
    def _delete():
        db.delete(db_transaction)
        db.commit()
        return True
    
    return execute_with_retry(_delete)

def get_transaction_summary(db: Session, user_id: int, month: int, year: int) -> dict:
    # Get total income and expenses for the specified month
    income_result = db.query(func.sum(Transaction.amount)).filter(
        and_(
            Transaction.user_id == user_id,
            Transaction.type == TransactionType.INCOME,
            func.extract('month', Transaction.date) == month,
            func.extract('year', Transaction.date) == year
        )
    ).scalar()
    
    expense_result = db.query(func.sum(Transaction.amount)).filter(
        and_(
            Transaction.user_id == user_id,
            Transaction.type == TransactionType.EXPENSE,
            func.extract('month', Transaction.date) == month,
            func.extract('year', Transaction.date) == year
        )
    ).scalar()
    
    total_income = Decimal(str(income_result or 0))
    total_expenses = Decimal(str(expense_result or 0))
    balance = total_income - total_expenses
    
    return {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "balance": balance,
        "month": month,
        "year": year
    } 