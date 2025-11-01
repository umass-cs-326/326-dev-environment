"""
FastAPI Dependencies

This file contains FastAPI dependency functions that handle authentication
and authorization for protected routes. Dependencies in FastAPI are functions
that run before your route handlers and can provide data or enforce requirements.

Key concepts:
- FastAPI dependency injection system
- OAuth2 Bearer token handling
- Automatic authentication for protected routes
- Error handling for invalid authentication
"""

from app.core.auth import decode_access_token
from app.core.config import TOKEN_URL
from app.db.database import get_user
from app.models.user import TokenData, User, UserInDB
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

# =============================================================================
# OAUTH2 SETUP
# =============================================================================

# OAuth2 scheme for handling Bearer tokens
# This tells FastAPI to look for tokens in the Authorization header
# The tokenUrl parameter tells clients where to get tokens
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=TOKEN_URL)


# =============================================================================
# AUTHENTICATION DEPENDENCIES
# =============================================================================

async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserInDB:
    """
    FastAPI dependency to get the current user from JWT token.

    This dependency is automatically called by FastAPI when a route
    uses it. It validates the JWT token and returns the user information.

    How it works:
    1. FastAPI extracts the token from the Authorization header
    2. We decode and validate the JWT token
    3. We look up the user in the database
    4. We return the user information for use in the route

    Args:
        token: JWT token automatically extracted by oauth2_scheme

    Returns:
        Current user information

    Raises:
        HTTPException: If token is invalid or user not found
    """
    # Create a standard exception for authentication failures
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decode the JWT token to get the payload
        payload = decode_access_token(token)
        if payload is None:
            raise credentials_exception

        # Extract the username from the token payload
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception

        # Create a TokenData object for validation
        token_data = TokenData(username=username)

    except JWTError:
        # Token is malformed or signature is invalid
        raise credentials_exception

    # Look up the user in the database
    user = get_user(username=token_data.username)
    if user is None:
        # User doesn't exist (maybe was deleted after token was issued)
        raise credentials_exception

    return user


async def get_current_active_user(current_user: UserInDB = Depends(get_current_user)) -> User:
    """
    FastAPI dependency to get current active (non-disabled) user.

    This builds on get_current_user to also check if the user account
    is active. This allows administrators to disable user accounts
    without deleting them.

    Args:
        current_user: User from get_current_user dependency

    Returns:
        Current active user (as public User model, not UserInDB)

    Raises:
        HTTPException: If user account is disabled
    """
    if current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User account is disabled"
        )

    # Convert UserInDB to User to remove sensitive data
    return User(
        username=current_user.username,
        email=current_user.email,
        full_name=current_user.full_name,
        disabled=current_user.disabled
    )


# =============================================================================
# OPTIONAL AUTHENTICATION DEPENDENCIES
# =============================================================================

async def get_current_user_optional(token: str = Depends(oauth2_scheme)) -> UserInDB | None:
    """
    Optional authentication dependency.

    This dependency returns the current user if a valid token is provided,
    but doesn't raise an error if no token or an invalid token is provided.
    Useful for routes that work differently for authenticated vs anonymous users.

    Args:
        token: JWT token (may be invalid or missing)

    Returns:
        User if token is valid, None otherwise
    """
    try:
        return await get_current_user(token)
    except HTTPException:
        return None


# =============================================================================
# PERMISSION-BASED DEPENDENCIES
# =============================================================================

def require_admin_user(current_user: User = Depends(get_current_active_user)) -> User:
    """
    Dependency that requires the current user to be an administrator.

    This is an example of how you might implement role-based access control.
    You could extend the User model to include roles or permissions.

    Args:
        current_user: Current authenticated user

    Returns:
        Current user if they are an admin

    Raises:
        HTTPException: If user is not an administrator
    """
    # For this example, let's say only users with "admin" in their username are admins
    # In a real app, you'd have a proper role system
    if "admin" not in current_user.username.lower():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrator privileges required"
        )
    return current_user


def require_premium_user(current_user: User = Depends(get_current_active_user)) -> User:
    """
    Dependency that requires the current user to have premium access.

    Another example of permission-based access control.

    Args:
        current_user: Current authenticated user

    Returns:
        Current user if they have premium access

    Raises:
        HTTPException: If user doesn't have premium access
    """
    # Example: Check if user has premium access
    # In a real app, this might check a subscription status
    if not current_user.email or not current_user.email.endswith("@premium.com"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Premium subscription required"
        )
    return current_user
