# auth.py
from fastapi import HTTPException, Request
from models import User
from passlib.context import CryptContext
from sqlmodel import Session, select

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.
    TODO: Implement this function
    """
    pass


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against a hashed password.
    TODO: Implement this function
    """
    pass


def get_current_user(request: Request, session: Session) -> User:
    """
    Get the current logged-in user from the session.
    Raises HTTPException(401) if not authenticated.
    TODO: Implement this function
    """
    pass
