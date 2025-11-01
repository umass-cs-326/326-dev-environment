"""
API Routes

This file contains all the API endpoint definitions (routes) for the authentication
system. Routes are the URLs that clients can call to interact with our API.

Key concepts:
- RESTful API design
- Authentication endpoints (login)
- Protected endpoints (user data)
- FastAPI route decorators and dependency injection
"""

from datetime import timedelta

from app.core.auth import authenticate_user, create_access_token
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.core.dependencies import get_current_active_user
from app.models.user import Token, User
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

# =============================================================================
# ROUTER SETUP
# =============================================================================

# Create a router for authentication-related routes
# Using a router allows us to organize routes and apply common prefixes or dependencies
router = APIRouter()


# =============================================================================
# AUTHENTICATION ROUTES
# =============================================================================

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()) -> Token:
    """
    User login endpoint that returns a JWT access token.

    This is the main authentication endpoint where users send their
    username and password to get an access token. The token can then
    be used to access protected routes.

    How to use this endpoint:
    1. Send a POST request to /token
    2. Include username and password in form data
    3. Receive an access token in the response
    4. Use the token in the Authorization header for protected routes

    Args:
        form_data: Form containing username and password (handled by FastAPI)

    Returns:
        Token response containing access_token and token_type

    Raises:
        HTTPException: If username or password is incorrect
    """
    # Try to authenticate the user with provided credentials
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        # Authentication failed - don't reveal whether username or password was wrong
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Authentication successful! Create an access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},  # "sub" stands for "subject" in JWT terms
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"  # This tells clients to use "Bearer <token>" in headers
    }


# =============================================================================
# PROTECTED USER ROUTES
# =============================================================================

@router.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)) -> User:
    """
    Get current user's information.

    This is a protected endpoint that returns information about the currently
    authenticated user. The user must provide a valid JWT token to access this.

    Example usage:
    GET /users/me
    Authorization: Bearer <your_jwt_token>

    Args:
        current_user: Automatically injected by FastAPI authentication dependency

    Returns:
        Current user's public information (no sensitive data)
    """
    return current_user


@router.get("/users/me/items/")
async def read_own_items(current_user: User = Depends(get_current_active_user)) -> list[dict]:
    """
    Get current user's items/resources.

    This is another protected endpoint that returns items or resources
    belonging to the currently authenticated user. This demonstrates
    how to create endpoints that return user-specific data.

    Args:
        current_user: Automatically injected by FastAPI authentication dependency

    Returns:
        List of items owned by the current user
    """
    # In a real application, you would query the database for items
    # owned by the current user. For this demo, we return mock data.
    return [
        {
            "item_id": "item_001",
            "name": "Sample Item",
            "description": "This is a sample item owned by the user",
            "owner": current_user.username,
            "created_at": "2024-01-01T00:00:00Z"
        },
        {
            "item_id": "item_002",
            "name": "Another Item",
            "description": "Another sample item",
            "owner": current_user.username,
            "created_at": "2024-01-02T00:00:00Z"
        }
    ]


# =============================================================================
# PUBLIC ROUTES (NO AUTHENTICATION REQUIRED)
# =============================================================================

@router.get("/public/info")
async def get_public_info() -> dict:
    """
    Get public information about the API.

    This endpoint doesn't require authentication and can be accessed by anyone.
    Useful for providing general information about your API.

    Returns:
        Public information about the API
    """
    return {
        "name": "Authentication Demo API",
        "version": "1.0.0",
        "description": "A demo API showing JWT authentication with FastAPI",
        "endpoints": {
            "login": "POST /token - Get access token with username/password",
            "profile": "GET /users/me - Get current user info (requires auth)",
            "items": "GET /users/me/items/ - Get user's items (requires auth)"
        },
        "authentication": "JWT Bearer tokens"
    }


# =============================================================================
# EXAMPLE ROUTES FOR DIFFERENT ACCESS LEVELS
# =============================================================================

@router.get("/users/me/profile/extended")
async def get_extended_profile(current_user: User = Depends(get_current_active_user)) -> dict:
    """
    Get extended user profile information.

    This demonstrates how you might have different endpoints that return
    different levels of detail about the user.

    Args:
        current_user: Current authenticated user

    Returns:
        Extended profile information
    """
    return {
        "basic_info": {
            "username": current_user.username,
            "email": current_user.email,
            "full_name": current_user.full_name
        },
        "account_status": {
            "disabled": current_user.disabled,
            "account_type": "premium" if current_user.email and "@premium.com" in current_user.email else "basic",
            "last_login": "2024-01-15T10:30:00Z"  # Mock data
        },
        "preferences": {
            "theme": "dark",
            "notifications": True,
            "language": "en"
        }
    }
