"""
Database Operations

This file handles all database-related operations for user management.
In a real application, this would connect to a proper database like PostgreSQL
or MongoDB. For learning purposes, we use a simple in-memory dictionary.

Key concepts:
- Data storage and retrieval
- User lookup operations
- Database abstraction (easy to swap out later)
"""

from typing import Optional

from app.models.user import UserInDB

# =============================================================================
# MOCK DATABASE
# =============================================================================

# In-memory "database" - In production, replace with real database
# This simulates what would normally be stored in a database table
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "john@example.com",
        # Password: "secret" - hashed with bcrypt
        # In production, you'd never store plain passwords!
        "hashed_password": "$2b$12$ukiUCP.QeMZNdLHNYzL1sugG6AOdLFFoLOFVzeRllTEL.5sXOMxgq",
        "disabled": False,
    }
}


# =============================================================================
# DATABASE OPERATIONS
# =============================================================================

def get_user(username: str) -> Optional[UserInDB]:
    """
    Retrieve a user from the database by username.

    This function abstracts database access so we can easily switch
    from our mock database to a real one later.

    Args:
        username: The username to look up

    Returns:
        UserInDB object if user exists, None if not found
    """
    if username in fake_users_db:
        user_dict = fake_users_db[username]
        return UserInDB(**user_dict)
    return None


def user_exists(username: str) -> bool:
    """
    Check if a user exists in the database.

    Args:
        username: The username to check

    Returns:
        True if user exists, False otherwise
    """
    return username in fake_users_db


def get_all_usernames() -> list[str]:
    """
    Get a list of all usernames in the database.

    Useful for administrative functions or debugging.

    Returns:
        List of all usernames
    """
    return list(fake_users_db.keys())


# =============================================================================
# FUTURE DATABASE FUNCTIONS
# =============================================================================

# These functions show how you might extend the database layer:

def create_user(user_data: dict) -> bool:
    """
    Create a new user in the database.

    Args:
        user_data: Dictionary containing user information

    Returns:
        True if user was created successfully, False if username already exists
    """
    username = user_data.get("username")
    if username and not user_exists(username):
        fake_users_db[username] = user_data
        return True
    return False


def update_user(username: str, user_data: dict) -> bool:
    """
    Update an existing user's information.

    Args:
        username: Username of user to update
        user_data: New user data

    Returns:
        True if user was updated, False if user doesn't exist
    """
    if user_exists(username):
        fake_users_db[username].update(user_data)
        return True
    return False


def delete_user(username: str) -> bool:
    """
    Delete a user from the database.

    Args:
        username: Username to delete

    Returns:
        True if user was deleted, False if user doesn't exist
    """
    if user_exists(username):
        del fake_users_db[username]
        return True
    return False
