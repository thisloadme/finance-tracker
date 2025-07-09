from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.deps import get_current_active_user
from app.crud.budget import (
    get_budget_category, get_budget_categories, create_budget_category,
    update_budget_category, delete_budget_category, get_budget_usage
)
from app.schemas.budget import BudgetCategory, BudgetCategoryCreate, BudgetCategoryUpdate

router = APIRouter()

@router.get("/budget-categories", response_model=List[BudgetCategory])
def read_budget_categories(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    categories = get_budget_categories(db, user_id=current_user.user_id, skip=skip, limit=limit)
    return categories

@router.post("/budget-categories", response_model=BudgetCategory)
def create_budget_category_endpoint(
    category: BudgetCategoryCreate,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    return create_budget_category(db=db, category=category, user_id=current_user.user_id)

@router.get("/budget-categories/{category_id}", response_model=BudgetCategory)
def read_budget_category(
    category_id: int,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    category = get_budget_category(db, category_id=category_id, user_id=current_user.user_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Budget category not found")
    return category

@router.put("/budget-categories/{category_id}", response_model=BudgetCategory)
def update_budget_category_endpoint(
    category_id: int,
    category_update: BudgetCategoryUpdate,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    category = update_budget_category(
        db=db, category_id=category_id, user_id=current_user.user_id, category_update=category_update
    )
    if category is None:
        raise HTTPException(status_code=404, detail="Budget category not found")
    return category

@router.delete("/budget-categories/{category_id}")
def delete_budget_category_endpoint(
    category_id: int,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    success = delete_budget_category(db=db, category_id=category_id, user_id=current_user.user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Budget category not found")
    return {"message": "Budget category deleted successfully"}

@router.get("/budget-categories/{category_id}/usage")
def get_budget_category_usage(
    category_id: int,
    month: int = Query(..., ge=1, le=12),
    year: int = Query(..., ge=2020),
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Check if category exists and belongs to user
    category = get_budget_category(db, category_id=category_id, user_id=current_user.user_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Budget category not found")
    
    usage = get_budget_usage(db, category_id=category_id, user_id=current_user.user_id, month=month, year=year)
    limit = category.monthly_limit

    usage = float(usage) if usage is not None else 0
    limit = float(limit) if limit is not None else 0
    
    return {
        "category_id": category_id,
        "category_name": category.name,
        "monthly_limit": limit,
        "usage": usage,
        "remaining": limit - usage,
        "percentage_used": (usage / limit * 100) if limit > 0 else 0,
        "month": month,
        "year": year
    } 