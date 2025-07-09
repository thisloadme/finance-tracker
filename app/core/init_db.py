from app.core.database import engine
from app.models import User, BudgetCategory, Transaction

def init_db():
    # Create all tables
    User.__table__.create(bind=engine, checkfirst=True)
    BudgetCategory.__table__.create(bind=engine, checkfirst=True)
    Transaction.__table__.create(bind=engine, checkfirst=True)

if __name__ == "__main__":
    init_db()
    print("Database tables created successfully!") 