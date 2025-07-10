from pydantic import BaseModel, validator, Field, condecimal
from typing import Optional
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP

class BudgetCategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    monthly_limit: Decimal = condecimal(ge=Decimal('0.01'), decimal_places=2)

    @validator('monthly_limit')
    def validate_limit(cls, v):
        if v <= 0:
            raise ValueError('Monthly limit must be greater than 0')
        return Decimal(str(v)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    @validator('name')
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError('Name cannot be empty or whitespace only')
        return v.strip()

class BudgetCategoryCreate(BudgetCategoryBase):
    pass

class BudgetCategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    monthly_limit: Optional[Decimal] = condecimal(ge=Decimal('0.01'), decimal_places=2)
    is_active: Optional[int] = None

    @validator('monthly_limit')
    def validate_limit(cls, v):
        if v is not None and v <= 0:
            raise ValueError('Monthly limit must be greater than 0')
        if v is not None:
            return Decimal(str(v)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        return v

    @validator('name')
    def validate_name(cls, v):
        if v is not None and not v.strip():
            raise ValueError('Name cannot be empty or whitespace only')
        return v.strip() if v is not None else v

class BudgetCategoryInDB(BudgetCategoryBase):
    category_id: int
    user_id: int
    is_active: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class BudgetCategory(BudgetCategoryInDB):
    pass 