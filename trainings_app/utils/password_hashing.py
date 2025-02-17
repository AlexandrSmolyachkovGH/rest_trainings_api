from passlib.context import CryptContext
from dotenv import load_dotenv
import os

load_dotenv()

hashing_algorithm = os.getenv("HASHING_ALGORITHM", "bcrypt")
deprecated_status = os.getenv("HASHING_DEPRECATED", "auto")

pwd_context = CryptContext(schemes=[hashing_algorithm], deprecated=deprecated_status)


def hash_password(password: str) -> str:
    """Generates a hashed password from the provided password."""
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """Returns the result of comparing the password with the hashed_password."""
    return pwd_context.verify(password, hashed_password)
