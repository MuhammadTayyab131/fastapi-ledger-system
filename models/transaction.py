# models/transaction.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey , DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


from database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)

    customer_id = Column(
        Integer,
        ForeignKey("customers.id"),
        nullable=False
    )

    amount = Column(Float, nullable=False)
    type = Column(String, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    customer = relationship(
        "Customer",
        back_populates="transactions"
    )