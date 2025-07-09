from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import create_access_token, create_refresh_token, get_password_hash
from app.crud.user import create_user, authenticate_user, get_user_by_email, create_token_reset_password, claim_token_reset_password, update_user
from app.schemas.auth import Token, LoginRequest, RefreshTokenRequest, PasswordResetRequest, PasswordResetConfirm
from app.schemas.user import UserCreate, User, UserUpdate
from app.core.deps import get_current_active_user
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/register", response_model=User)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    return create_user(db=db, user=user)

@router.post("/login", response_model=Token)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, login_data.username, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(data={"sub": user.username})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/refresh", response_model=Token)
def refresh_token(refresh_data: RefreshTokenRequest, db: Session = Depends(get_db)):
    from app.core.security import verify_token
    
    payload = verify_token(refresh_data.refresh_token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    username: str = payload.get("sub")
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    user = get_user_by_email(db, email=username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    new_refresh_token = create_refresh_token(data={"sub": user.username})
    
    return {
        "access_token": access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }

@router.post("/password-reset-request")
def request_password_reset(reset_request: PasswordResetRequest, db: Session = Depends(get_db)):
    user = get_user_by_email(db, email=reset_request.email)
    if user:
        token = create_token_reset_password(db, user.user_id)
        return {
            "reset_token": token,
            "message": "User found"
        }
    
    return {"reset_token": None, "message": "User not found"}

@router.post("/password-reset-confirm")
def confirm_password_reset(reset_confirm: PasswordResetConfirm, db: Session = Depends(get_db)):
    user = claim_token_reset_password(db, reset_confirm.token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    
    updated_user = update_user(db, user.user_id, UserUpdate(password=reset_confirm.new_password))
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to reset password"
        )
    
    return {"message": "Password has been reset successfully", "user": updated_user}

@router.get("/me", response_model=User)
def read_users_me(current_user = Depends(get_current_active_user)):
    return current_user 