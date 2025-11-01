"""
Authentication and Security

This file contains all the authentication logic, password handling,
and JWT token operations. This is the core security module that handles
the cryptographic operations needed for secure authentication.

Key concepts:
- Password hashing and verification with bcrypt
- JWT token creation and validation
- User authentication workflow
- Security best practices
"""

from datetime import datetime, timedelta, timezone
from typing import Any, Optional

from app.core.config import ALGORITHM, SECRET_KEY
from app.db.database import get_user
from app.models.user import UserInDB
from jose import ExpiredSignatureError, JWTError, jwt
from passlib.context import CryptContext

# =============================================================================
# PASSWORD SECURITY SETUP
# =============================================================================

# Password hashing context using bcrypt
# Bcrypt is a secure hashing algorithm designed for passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# =============================================================================
# PASSWORD OPERATIONS
# =============================================================================

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.

    This function safely compares a user's input password with the stored
    hashed version. It uses constant-time comparison to prevent timing attacks.

    Args:
        plain_password: The plain text password to verify
        hashed_password: The hashed password from the database

    Returns:
        True if passwords match, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash a plain password using bcrypt.

    This creates a secure hash of a password that can be safely stored
    in the database. Each hash includes a random salt automatically.

    Args:
        password: The plain text password to hash

    Returns:
        The securely hashed password string
    """
    return pwd_context.hash(password)


# =============================================================================
# USER AUTHENTICATION
# =============================================================================

def authenticate_user(username: str, password: str) -> Optional[UserInDB]:
    """
    Authenticate a user by username and password.

    This is the main authentication function that:
    1. Looks up the user in the database
    2. Verifies their password
    3. Returns the user if authentication succeeds

    Args:
        username: The username to authenticate
        password: The plain text password

    Returns:
        UserInDB object if authentication successful, None otherwise
    """
    # First, try to get the user from the database
    user = get_user(username)
    if not user:
        # User doesn't exist
        return None

    # Check if the password is correct
    if not verify_password(password, user.hashed_password):
        # Password is incorrect
        return None

    # Authentication successful!
    return user


# =============================================================================
# JWT TOKEN OPERATIONS
# =============================================================================

def create_access_token(data: dict[str, str | datetime], expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.

    JWT (JSON Web Token) is a secure way to transmit information between
    parties. The token contains user information and an expiration time,
    and is signed with our secret key so it can't be tampered with.

    Args:
        data: The data to encode in the token (typically username)
        expires_delta: Optional custom expiration time

    Returns:
        Encoded JWT token string
    """
    # Make a copy of the data to avoid modifying the original
    to_encode = data.copy()

    # Set when the token expires
    if expires_delta:
        # Use the provided expiration time
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        # Default to 15 minutes from now
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    # Add the expiration time to the token payload
    to_encode.update({"exp": expire})

    # Create the JWT token using our secret key and algorithm
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict[str, Any]]:
    """
    Decode and validate a JWT access token.

    This function verifies that a token is valid and hasn't been tampered with.
    If the token is valid, it returns the payload data.

    Args:
        token: The JWT token to decode

    Returns:
        Token payload if valid, None if invalid or expired
    """
    try:
        # Decode the token using our secret key
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except ExpiredSignatureError:
        # Token has expired
        return None
    except JWTError:
        # Token is invalid (wrong signature, malformed, etc.)
        return None


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def get_username_from_token(token: str) -> Optional[str]:
    """
    Extract username from a JWT token.

    This is a convenience function that decodes a token and extracts
    the username from the payload.

    Args:
        token: JWT token string

    Returns:
        Username if token is valid, None otherwise
    """
    payload = decode_access_token(token)
    if payload:
        # "sub" is the standard JWT field for subject (username)
        return payload.get("sub")
    return None


def is_token_expired(token: str) -> bool:
    """
    Check if a JWT token has expired.

    Args:
        token: JWT token string

    Returns:
        True if token is expired or invalid, False if still valid
    """
    payload = decode_access_token(token)
    return payload is None
