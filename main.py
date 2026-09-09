from fastapi import FastAPI

from database import Base, engine
from models.customer import Customer
from routes.customer import router as customer_router


Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(customer_router)

@app.get("/")
def root():
    return {"message": "Welcome to Ledger System!"}