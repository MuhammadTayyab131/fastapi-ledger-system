# routes/admin.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import SessionLocal
from models.user import User
from schemas.user import (
    UserRole,
    ShopkeeperCustomersResponse
)
from dependencies.auth import require_role


router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)


# Database connection
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# Get all shopkeepers and their customers
@router.get(
    "/shopkeepers/customers",
    response_model=list[ShopkeeperCustomersResponse]
)
def get_shopkeepers_customers(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role(UserRole.admin)
    )
):
    shopkeepers = db.query(User).filter(
        User.role == UserRole.shopkeeper.value
    ).order_by(User.id).all()

    result = []

    for shopkeeper in shopkeepers:
        result.append(
            ShopkeeperCustomersResponse(
                shopkeeper_id=shopkeeper.id,
                shopkeeper_name=shopkeeper.username,
                customers=shopkeeper.customers
            )
        )

    return result