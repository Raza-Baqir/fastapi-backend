from passlib.context import CryptContext

# Initialize password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify that the provided plain password matches the hashed password.
    """
    return pwd_context.verify(plain_password, hashed_password)
