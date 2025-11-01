"""
Data Models

This file defines all the data structures (models) used in the authentication system.
These models define the shape of data that flows through our API.

Key concepts:
- Pydantic models for data validation
- Separation of public and private data (User vs UserInDB)
- Type safety with Python type hints
"""

from typing import Optional

from pydantic import BaseModel

# =============================================================================
# AUTHENTICATION MODELS
# =============================================================================


class Token(BaseModel):
    """
    Response model for the login endpoint.

    This is what gets returned when a user successfully logs in.
    Contains the JWT token and its type.
    """
    access_token: str  # The actual JWT token string
    token_type: str    # Usually "bearer" for Bearer token authentication


class TokenData(BaseModel):
    """
    Internal model for JWT token payload data.

    This represents the data we extract from a JWT token when validating it.
    Used internally by the authentication system.
    """
    username: Optional[str] = None  # Username extracted from token


# =============================================================================
# USER MODELS
# =============================================================================

class User(BaseModel):
    """
    Public user model for API responses.

    This model excludes sensitive information like passwords.
    Used when returning user data through API endpoints.
    """
    username: str                        # Unique username
    email: Optional[str] = None          # User's email address (optional)
    full_name: Optional[str] = None      # User's display name (optional)
    disabled: Optional[bool] = None      # Whether the account is disabled


class UserInDB(User):
    """
    Database user model that includes sensitive data.

    This extends the public User model to include the hashed password.
    Used internally for database operations and authentication.
    Never returned through API endpoints!
    """
    hashed_password: str  # Bcrypt-hashed password (never store plain passwords!)
