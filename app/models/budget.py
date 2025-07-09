from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, Boolean, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class BudgetCategory(Base):
    __tablename__ = "category"

    category_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(String(500))
    monthly_limit = Column(Numeric(10, 2), nullable=False)  # Decimal with 2 places
    color = Column(String(7), default="#000000")  # Hex color for UI
    is_active = Column(Integer, default=1)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="category")
    transactions = relationship("Transaction", back_populates="category")

    # Indexes for performance
    __table_args__ = (
        Index('idx_budget_user_active', 'user_id', 'is_active'),
        Index('idx_budget_name_user', 'name', 'user_id'),
    ) 