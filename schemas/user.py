# schemas/user.py

from enum import Enum

from pydantic import BaseModel

class UserRole(str, Enum):
    shopkeeper = "shopkeeper"
    admin = "admin"

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    role: UserRole

    class Config:
        from_attributes = True

# Admin response schemas

from pydantic import BaseModel, ConfigDict


class AdminCustomerResponse(BaseModel):
    id: int
    name: str
    phone: str | None = None
    email: str | None = None

    model_config = ConfigDict(from_attributes=True)


class ShopkeeperCustomersResponse(BaseModel):
    shopkeeper_id: int
    shopkeeper_name: str
    customers: list[AdminCustomerResponse]