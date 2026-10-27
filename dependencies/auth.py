# dependencies/auth.py

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from database import SessionLocal
from models.user import User
from schemas.user import UserRole
from utils.jwt_handler import verify_access_token


# Read the JWT token from the Authorization header
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


# Database connection
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# Identify the currently logged-in user
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    payload = verify_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    username = payload.get("sub")

    if username is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    user = db.query(User).filter(
        User.username == username
    ).first()

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return user


# Allow access only to users with the required roles
def require_role(*required_roles: UserRole):

    def role_checker(
        current_user: User = Depends(get_current_user)
    ):
        allowed_roles = [
            role.value for role in required_roles
        ]

        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=403,
                detail="You do not have permission to perform this action"
            )

        return current_user

    return role_checker