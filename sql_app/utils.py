from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# define function to create hash password
def hash(password: str):
    return pwd_context.hash(password)


# define function to verify login password and registered password
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
