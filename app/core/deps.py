from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import verify_token
from app.crud.user import get_user_by_username
from app.schemas.auth import TokenData

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = verify_token(credentials.credentials)
    if payload is None:
        raise credentials_exception
    
    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception
    
    token_data = TokenData(username=username)
    user = get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    
    return user

def get_current_active_user(current_user = Depends(get_current_user)):
    if current_user.is_active != 1:
        raise HTTPException(status_code=400, detail="Inactive user")
    if current_user.is_verified != 1 and current_user.role != "admin":
        raise HTTPException(status_code=400, detail="Unverified user")
    return current_user 