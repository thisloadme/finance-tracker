from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, Enum, Text, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from app.core.database import Base

class TransactionType(enum.Enum):
    INCOME = "income"
    EXPENSE = "expense"

class Transaction(Base):
    __tablename__ = "transaction"

    transaction_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    category_id = Column(Integer, ForeignKey("category.category_id"), nullable=True)
    type = Column(Enum(TransactionType), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)  # Decimal with 2 places
    description = Column(String(500), nullable=False)
    date = Column(DateTime, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="transactions")
    category = relationship("BudgetCategory", back_populates="transactions")

    # Indexes for performance
    __table_args__ = (
        Index('idx_transaction_user_date', 'user_id', 'date'),
        Index('idx_transaction_category', 'category_id'),
        Index('idx_transaction_type', 'type'),
        Index('idx_transaction_description', 'description'),
    ) 