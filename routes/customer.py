# routes/customer.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal

from models.customer import Customer
from models.transaction import Transaction
from models.user import User

from schemas.customer import (
    CustomerCreate,
    CustomerResponse,
    CustomerUpdate,
    CustomerBalanceResponse,
    CustomerStatementResponse
)

from schemas.transaction import TransactionResponse
from schemas.user import UserRole
from dependencies.auth import require_role


router = APIRouter(
    prefix="/customers",
    tags=["customers"]
)


# Database connection
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# Get a customer only if the logged-in shopkeeper owns it
def get_owned_customer(
    customer_id: int,
    db: Session,
    current_user: User
):
    customer = db.query(Customer).filter(
        Customer.id == customer_id,
        Customer.owner_id == current_user.id
    ).first()

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return customer


# Create a customer
@router.post("/", response_model=CustomerResponse)
def create_customer(
    customer: CustomerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role(UserRole.shopkeeper)
    )
):
    new_customer = Customer(
        name=customer.name,
        phone=customer.phone,
        email=customer.email,
        owner_id=current_user.id
    )

    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)

    return new_customer


# Get only the logged-in shopkeeper's customers
@router.get("/", response_model=list[CustomerResponse])
def get_customers(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role(UserRole.shopkeeper)
    )
):
    customers = db.query(Customer).filter(
        Customer.owner_id == current_user.id
    ).all()

    return customers


# Get one customer
@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role(UserRole.shopkeeper)
    )
):
    return get_owned_customer(
        customer_id,
        db,
        current_user
    )


# Update a customer
@router.put("/{customer_id}", response_model=CustomerResponse)
def update_customer(
    customer_id: int,
    customer_data: CustomerUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role(UserRole.shopkeeper)
    )
):
    customer = get_owned_customer(
        customer_id,
        db,
        current_user
    )

    updated_data = customer_data.model_dump(
        exclude_unset=True
    )

    for key, value in updated_data.items():
        setattr(customer, key, value)

    db.commit()
    db.refresh(customer)

    return customer


# Delete a customer
@router.delete("/{customer_id}")
def delete_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role(UserRole.shopkeeper)
    )
):
    customer = get_owned_customer(
        customer_id,
        db,
        current_user
    )

    db.delete(customer)
    db.commit()

    return {
        "message": "Customer deleted successfully"
    }


# Get all transactions for an owned customer
@router.get(
    "/{customer_id}/transactions",
    response_model=list[TransactionResponse]
)
def get_customer_transactions(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role(UserRole.shopkeeper)
    )
):
    customer = get_owned_customer(
        customer_id,
        db,
        current_user
    )

    return customer.transactions


# Get one transaction belonging to an owned customer
@router.get(
    "/{customer_id}/transactions/{transaction_id}",
    response_model=TransactionResponse
)
def get_customer_transaction(
    customer_id: int,
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role(UserRole.shopkeeper)
    )
):
    # First verify that the customer belongs to this shopkeeper
    get_owned_customer(
        customer_id,
        db,
        current_user
    )

    transaction = db.query(Transaction).filter(
        Transaction.id == transaction_id,
        Transaction.customer_id == customer_id
    ).first()

    if not transaction:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    return transaction


# Get an owned customer's balance
@router.get(
    "/{customer_id}/balance",
    response_model=CustomerBalanceResponse
)
def get_customer_balance(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role(UserRole.shopkeeper)
    )
):
    customer = get_owned_customer(
        customer_id,
        db,
        current_user
    )

    balance = sum(
        transaction.amount
        if transaction.type == "credit"
        else -transaction.amount
        for transaction in customer.transactions
    )

    return CustomerBalanceResponse(
        customer_id=customer.id,
        balance=balance
    )


# Get an owned customer's statement
@router.get(
    "/{customer_id}/statement",
    response_model=CustomerStatementResponse
)
def get_customer_statement(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role(UserRole.shopkeeper)
    )
):
    customer = get_owned_customer(
        customer_id,
        db,
        current_user
    )

    total_credit = sum(
        transaction.amount
        for transaction in customer.transactions
        if transaction.type == "credit"
    )

    total_debit = sum(
        transaction.amount
        for transaction in customer.transactions
        if transaction.type == "debit"
    )

    total_balance = total_credit - total_debit

    return CustomerStatementResponse(
        customer_id=customer.id,
        total_credit=total_credit,
        total_debit=total_debit,
        total_balance=total_balance,
        transactions_list=customer.transactions
    )