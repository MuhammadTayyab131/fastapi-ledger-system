# routes/customer.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session


from database import SessionLocal
from models.customer import Customer
from schemas.customer import CustomerCreate , CustomerResponse , CustomerUpdate

router = APIRouter(
    prefix="/customers",
    tags=["customers"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#create a new customer

@router.post("/", response_model=CustomerResponse)
def create_customer(
    customer: CustomerCreate, 
    db: Session = Depends(get_db)
):

    new_customer = Customer(
        name=customer.name,
        phone=customer.phone,
        email=customer.email
    )

    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)

    return new_customer

# get all the customers

@router.get("/", response_model=list[CustomerResponse])
def get_customers(
    db: Session = Depends(get_db)
):
    customers = db.query(Customer).all()
    return customers

# get a customer by id

@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer(
    customer_id: int,
    db: Session = Depends(get_db)
):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail= "Customer not found")

    return customer


# update customer by id

@router.put("/{customer_id}", response_model=CustomerUpdate)
def update_customer(
    customer_id: int,
    customer_data: CustomerUpdate,
    db: Session = Depends(get_db)
):
    customer = db.query(Customer).filter(
        Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(
            status_code=404,
            detail="customer not found")

    updated_data = customer_data.dict(exclude_unset=True)
    for key, value in updated_data.items():
        setattr(customer, key, value)

    db.commit()
    db.refresh(customer)

    return customer

# delete customer by id

@router.delete("/{customer_id}")
def delete_customer(
    customer_id: int,
    db: Session = Depends(get_db)
):
    customer = db.query(Customer).filter(
        Customer.id == customer_id).first()

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="customer not found"
        )

    db.delete(customer)
    db.commit()

    return{
        "Customer deleted successfully"
    }