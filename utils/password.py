# utils/password.py


from passlib.context import CryptContext


# creating password context

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


# creating hash password

def hash_password(password):
    return pwd_context.hash(password)


# creating password verification

def verify_password(password, hashed_password):
    return pwd_context.verify(
        password,
        hashed_password
    )