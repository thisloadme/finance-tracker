from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.deps import get_current_active_user
from app.crud.user import get_user, update_user, delete_user, get_users, create_user
from app.schemas.user import User, UserUpdate, UserCreate

router = APIRouter()

@router.get("/users", response_model=List[User])
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    users = get_users(db, skip=skip, limit=limit)
    return users

@router.get("/user/{user_id}", response_model=User)
def read_user(
    user_id: int, 
    db: Session = Depends(get_db), 
    current_user = Depends(get_current_active_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/user", response_model=User)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    user = create_user(db, user)
    return user

@router.put("/user/{user_id}", response_model=User)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    updated_user = update_user(db, user_id, user_update)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.delete("/user/{user_id}", response_model=User)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    success = delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}

@router.get("/users/me", response_model=User)
def read_user_me(current_user = Depends(get_current_active_user)):
    return current_user

@router.put("/users/me", response_model=User)
def update_user_me(
    user_update: UserUpdate,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    updated_user = update_user(db=db, user_id=current_user.user_id, user_update=user_update)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user