# schemas/customer.py

from pydantic import BaseModel
from schemas.transaction import TransactionResponse


# customer schema for creating a new customer

class CustomerCreate(BaseModel):
    name: str
    phone: str | None = None
    email: str | None = None


# customer schema for response model

class CustomerResponse(CustomerCreate):
    id: int
    name: str
    phone: str | None = None
    email: str | None = None

    class Config:
        from_attributes = True


# customer schema for updating a customer

class CustomerUpdate(BaseModel):
    name: str | None = None
    phone: str | None = None
    email: str | None = None


# customer's balance schema

class CustomerBalanceResponse(BaseModel):
    customer_id: int
    balance: float


# customer's statement schema

class CustomerStatementResponse(BaseModel):
    customer_id: int
    total_credit: float
    total_debit: float
    total_balance: float
    transactions_list: list[TransactionResponse]