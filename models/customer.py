#models/customer.py

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    email = Column(String, nullable=True)
    

    # shopkeeper who owns the customer
    owner_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    # relationship with the user model

    owner = relationship(
        "User",
        back_populates="customers"
    )

    # relationship with the transaction model

    transactions = relationship(
        "Transaction",
        back_populates="customer"
    )

