"""
Application Configuration

This file contains all the configuration settings and constants used throughout
the authentication system. By centralizing configuration here, we make it easy
to modify settings without hunting through multiple files.

Key concepts:
- Centralized configuration management
- Security settings for JWT tokens
- Application constants
"""

# =============================================================================
# JWT (JSON Web Token) CONFIGURATION
# =============================================================================

# Secret key used to sign JWT tokens - NEVER expose this in production!
# In a real application, this should be loaded from environment variables
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"

# Algorithm used to sign JWT tokens (HS256 is HMAC with SHA-256)
ALGORITHM = "HS256"

# How long access tokens remain valid (in minutes)
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# =============================================================================
# APPLICATION CONFIGURATION
# =============================================================================

# FastAPI application metadata
APP_TITLE = "Authentication Demo"
APP_DESCRIPTION = "JWT Authentication with FastAPI"

# OAuth2 token URL - this is where clients will send login requests
TOKEN_URL = "token"
