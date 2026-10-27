# schemas/transaction.py

from enum import Enum
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


# Allowed transaction types
class TransactionType(str, Enum):
    credit = "credit"
    debit = "debit"


# Data required to create a transaction
class TransactionCreate(BaseModel):
    customer_id: int
    amount: float = Field(gt=0)
    type: TransactionType
    description: str | None = None


# Data returned to the client
class TransactionResponse(BaseModel):
    id: int
    customer_id: int
    amount: float
    type: TransactionType
    description: str | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Data allowed when updating a transaction
class TransactionUpdate(BaseModel):
    amount: float | None = Field(default=None, gt=0)
    type: TransactionType | None = None
    description: str | None = None