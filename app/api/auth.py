from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import create_access_token, create_refresh_token, get_password_hash
from app.crud.user import create_user, authenticate_user, get_user_by_email
from app.schemas.auth import Token, LoginRequest, RefreshTokenRequest, PasswordResetRequest, PasswordResetConfirm
from app.schemas.user import UserCreate, User
from app.core.deps import get_current_active_user

router = APIRouter()

@router.post("/register", response_model=User)
def register(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    # Create new user
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
    # In a real application, you would send an email with reset link
    # For now, just return success message
    user = get_user_by_email(db, email=reset_request.email)
    if user:
        # TODO: Send email with reset token
        return {"message": "If email exists, password reset instructions have been sent"}
    
    # Don't reveal if email exists or not for security
    return {"message": "If email exists, password reset instructions have been sent"}

@router.post("/password-reset-confirm")
def confirm_password_reset(reset_confirm: PasswordResetConfirm, db: Session = Depends(get_db)):
    # In a real application, you would verify the reset token
    # For now, just return success message
    # TODO: Implement token verification and password update
    return {"message": "Password has been reset successfully"}

@router.get("/me", response_model=User)
def read_users_me(current_user = Depends(get_current_active_user)):
    return current_user 