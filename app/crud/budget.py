from sqlalchemy.orm import Session
from app.models.budget import BudgetCategory
from app.schemas.budget import BudgetCategoryCreate, BudgetCategoryUpdate
from typing import List, Optional

def get_budget_category(db: Session, category_id: int, user_id: int) -> Optional[BudgetCategory]:
    return db.query(BudgetCategory).filter(
        BudgetCategory.category_id == category_id,
        BudgetCategory.user_id == user_id
    ).first()

def get_budget_categories(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[BudgetCategory]:
    return db.query(BudgetCategory).filter(
        BudgetCategory.user_id == user_id
    ).offset(skip).limit(limit).all()

def create_budget_category(db: Session, category: BudgetCategoryCreate, user_id: int) -> BudgetCategory:
    db_category = BudgetCategory(
        **category.dict(),
        user_id=user_id
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def update_budget_category(db: Session, category_id: int, user_id: int, category_update: BudgetCategoryUpdate) -> Optional[BudgetCategory]:
    db_category = get_budget_category(db, category_id, user_id)
    if not db_category:
        return None
    
    update_data = category_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_category, field, value)
    
    db.commit()
    db.refresh(db_category)
    return db_category

def delete_budget_category(db: Session, category_id: int, user_id: int) -> bool:
    db_category = get_budget_category(db, category_id, user_id)
    if not db_category:
        return False
    
    db.delete(db_category)
    db.commit()
    return True

def get_budget_usage(db: Session, category_id: int, user_id: int, month: int, year: int) -> float:
    from app.models.transaction import Transaction, TransactionType
    from sqlalchemy import func
    
    # Get total expenses for this category in the specified month
    total = db.query(func.sum(Transaction.amount)).filter(
        Transaction.category_id == category_id,
        Transaction.user_id == user_id,
        Transaction.type == TransactionType.EXPENSE,
        func.extract('month', Transaction.date) == month,
        func.extract('year', Transaction.date) == year
    ).scalar()
    
    return total or 0.0 