# models/user.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(
        String,
        unique=True,
        nullable=False
    )

    password = Column(
        String,
        nullable=False
    )

    role = Column(
        String,
        default="shopkeeper",
        nullable=False
    )

    # customer owned by the shopkeeper
    customers = relationship(
        "Customer",
        back_populates="owner"
    )