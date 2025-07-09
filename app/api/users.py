from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.deps import get_current_active_user
from app.crud.user import get_user, update_user, delete_user
from app.schemas.user import User, UserUpdate

router = APIRouter()

@router.get("/users/me", response_model=User)
def read_user_me(current_user = Depends(get_current_active_user)):
    return current_user

@router.put("/users/me", response_model=User)
def update_user_me(
    user_update: UserUpdate,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    updated_user = update_user(db=db, user_id=current_user.user_id, user_update=user_update)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.delete("/users/me")
def delete_user_me(
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    success = delete_user(db=db, user_id=current_user.user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"} 