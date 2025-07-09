from pydantic import BaseModel, validator, Field
from typing import Optional
from datetime import datetime, date
from decimal import Decimal, ROUND_HALF_UP
from app.models.transaction import TransactionType

class TransactionBase(BaseModel):
    type: TransactionType
    amount: Decimal = Field(..., ge=Decimal('0.01'), decimal_places=2)
    description: str = Field(..., min_length=1, max_length=500)
    date: datetime = Field(..., description="Transaction date and time")
    category_id: Optional[int] = Field(None, gt=0)

    @validator('amount')
    def validate_amount(cls, v):
        if v <= 0:
            raise ValueError('Amount must be greater than 0')
        # Round to 2 decimal places for currency
        return Decimal(str(v)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    @validator('description')
    def validate_description(cls, v):
        if not v.strip():
            raise ValueError('Description cannot be empty or whitespace only')
        return v.strip()

    @validator('date')
    def validate_date(cls, v):
        # Ensure date is not in the future
        if v.replace(tzinfo=None) > datetime.utcnow():
            raise ValueError('Transaction date cannot be in the future')
        return v

class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(BaseModel):
    type: Optional[TransactionType] = None
    amount: Optional[Decimal] = Field(None, ge=Decimal('0.01'), decimal_places=2)
    description: Optional[str] = Field(None, min_length=1, max_length=500)
    date: Optional[datetime] = None
    category_id: Optional[int] = Field(None, gt=0)

    @validator('amount')
    def validate_amount(cls, v):
        if v is not None and v <= 0:
            raise ValueError('Amount must be greater than 0')
        if v is not None:
            return Decimal(str(v)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        return v

    @validator('description')
    def validate_description(cls, v):
        if v is not None and not v.strip():
            raise ValueError('Description cannot be empty or whitespace only')
        return v.strip() if v is not None else v

    @validator('date')
    def validate_date(cls, v):
        if v is not None and v.replace(tzinfo=None) > datetime.utcnow():
            raise ValueError('Transaction date cannot be in the future')
        return v

class TransactionInDB(TransactionBase):
    transaction_id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Transaction(TransactionInDB):
    pass

class TransactionSummary(BaseModel):
    total_income: Decimal = Field(..., decimal_places=2)
    total_expenses: Decimal = Field(..., decimal_places=2)
    balance: Decimal = Field(..., decimal_places=2)
    month: int
    year: int 