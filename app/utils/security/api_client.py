"""
    Utilities for managing API client authentication.
"""

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_api_key(api_key: str) -> str:
    return pwd_context.hash(api_key)

def verify_api_key(api_key: str, hashed_api_key: str) -> bool:
    return pwd_context.verify(api_key, hashed_api_key)