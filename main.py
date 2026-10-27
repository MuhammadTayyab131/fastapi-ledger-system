from fastapi import FastAPI

from database import Base, engine

from models.customer import Customer
from models.transaction import Transaction
from models.user import User

from routes.customer import router as customer_router
from routes.transaction import router as transaction_router
from routes.auth import router as auth_router
from routes.admin import router as admin_router


Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(customer_router)
app.include_router(transaction_router)
app.include_router(auth_router)
app.include_router(admin_router)

@app.get("/")
def root():
    return {"message": "Welcome to Ledger System!"}