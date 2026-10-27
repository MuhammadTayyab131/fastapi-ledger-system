# routes/transaction.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal

from models.transaction import Transaction
from models.customer import Customer

from schemas.transaction import (
    TransactionCreate,
    TransactionResponse,
    TransactionUpdate
)

from schemas.user import UserRole
from dependencies.auth import require_role


router = APIRouter(
    prefix="/transactions",
    tags=["transactions"]
)


# Database connection
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# Only authenticated shopkeepers can access transaction routes
shopkeeper_access = Depends(
    require_role(UserRole.shopkeeper)
)


# Create a transaction
@router.post("/", response_model=TransactionResponse)
def create_transaction(
    transaction: TransactionCreate,
    db: Session = Depends(get_db),
    current_user=shopkeeper_access
):
    # Check whether the customer exists
    customer = db.query(Customer).filter(
        Customer.id == transaction.customer_id
    ).first()

    if not customer:
        raise HTTPException(
            status_code=404,
            detail=f"Customer with id {transaction.customer_id} not found"
        )

    # Create the transaction
    new_transaction = Transaction(
        customer_id=transaction.customer_id,
        amount=transaction.amount,
        type=transaction.type.value,
        description=transaction.description
    )

    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)

    return new_transaction


# Get a single transaction
@router.get("/{transaction_id}", response_model=TransactionResponse)
def get_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user=shopkeeper_access
):
    transaction = db.query(Transaction).filter(
        Transaction.id == transaction_id
    ).first()

    if not transaction:
        raise HTTPException(
            status_code=404,
            detail=f"Transaction with id {transaction_id} not found"
        )

    return transaction


# Get all transactions
@router.get("/", response_model=list[TransactionResponse])
def get_transactions(
    db: Session = Depends(get_db),
    current_user=shopkeeper_access
):
    transactions = db.query(Transaction).all()

    return transactions


# Update a transaction
@router.patch("/{transaction_id}", response_model=TransactionResponse)
def update_transaction(
    transaction_id: int,
    transaction_update: TransactionUpdate,
    db: Session = Depends(get_db),
    current_user=shopkeeper_access
):
    transaction = db.query(Transaction).filter(
        Transaction.id == transaction_id
    ).first()

    if not transaction:
        raise HTTPException(
            status_code=404,
            detail=f"Transaction with id {transaction_id} not found"
        )

    # Update the amount if provided
    if transaction_update.amount is not None:
        transaction.amount = transaction_update.amount

    # Update the transaction type if provided
    if transaction_update.type is not None:
        transaction.type = transaction_update.type.value

    # Update the description if provided
    if transaction_update.description is not None:
        transaction.description = transaction_update.description

    db.commit()
    db.refresh(transaction)

    return transaction


# Delete a transaction
@router.delete("/{transaction_id}")
def delete_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user=shopkeeper_access
):
    transaction = db.query(Transaction).filter(
        Transaction.id == transaction_id
    ).first()

    if not transaction:
        raise HTTPException(
            status_code=404,
            detail=f"Transaction with id {transaction_id} not found"
        )

    db.delete(transaction)
    db.commit()

    return {
        "message": "Transaction deleted successfully"
    }

