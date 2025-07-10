from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from app.core.database import get_db
from app.core.deps import get_current_active_user
from app.core.exceptions import ValidationError, NotFoundError
from app.crud.transaction import (
    get_transaction, get_transactions, create_transaction,
    update_transaction, delete_transaction, get_transaction_summary
)
from app.schemas.transaction import Transaction, TransactionCreate, TransactionUpdate, TransactionSummary
from app.models.transaction import TransactionType

router = APIRouter()

@router.get("/transactions", response_model=List[Transaction])
def read_transactions(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    category_id: Optional[int] = Query(None),
    transaction_type: Optional[TransactionType] = Query(None),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    search: Optional[str] = Query(None),
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    transactions = get_transactions(
        db=db,
        user_id=current_user.user_id,
        skip=skip,
        limit=limit,
        category_id=category_id,
        transaction_type=transaction_type,
        start_date=start_date,
        end_date=end_date,
        search=search
    )
    return transactions

@router.post("/transaction", response_model=Transaction)
def create_transaction_endpoint(
    transaction: TransactionCreate,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    try:
        return create_transaction(db=db, transaction=transaction, user_id=current_user.user_id)
    except ValueError as e:
        raise ValidationError(str(e))

@router.get("/transaction/{transaction_id}", response_model=Transaction)
def read_transaction(
    transaction_id: int,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    transaction = get_transaction(db, transaction_id=transaction_id, user_id=current_user.user_id)
    if transaction is None:
        raise NotFoundError("Transaction not found")
    return transaction

@router.put("/transaction/{transaction_id}", response_model=Transaction)
def update_transaction_endpoint(
    transaction_id: int,
    transaction_update: TransactionUpdate,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    transaction = update_transaction(
        db=db, transaction_id=transaction_id, user_id=current_user.user_id, transaction_update=transaction_update
    )
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction

@router.delete("/transaction/{transaction_id}")
def delete_transaction_endpoint(
    transaction_id: int,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    success = delete_transaction(db=db, transaction_id=transaction_id, user_id=current_user.user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return {"message": "Transaction deleted successfully"}

@router.get("/transaction/summary/monthly", response_model=TransactionSummary)
def get_monthly_summary(
    month: int = Query(..., ge=1, le=12),
    year: int = Query(..., ge=2020),
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    from app.core.cache import cache
    
    cache_key = f"summary:{current_user.user_id}:{year}:{month}"
    cached_summary = cache.get(cache_key)
    
    if cached_summary:
        return TransactionSummary(**cached_summary)
    
    summary = get_transaction_summary(db=db, user_id=current_user.user_id, month=month, year=year)
    
    cache.set(cache_key, summary, expire=300)
    
    return TransactionSummary(**summary) 