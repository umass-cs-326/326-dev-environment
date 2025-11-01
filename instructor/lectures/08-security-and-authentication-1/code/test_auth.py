#!/usr/bin/env python3

"""
Simple test to verify the authentication system works correctly
"""

from main import authenticate_user, fake_users_db
import os
import sys

# Add current directory to path so we can import main
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def test_authentication():
    """Test the authentication function directly"""
    print("Testing authentication system...")

    # Test correct credentials
    user = authenticate_user(fake_users_db, "johndoe", "secret")
    if user:
        print("✅ Authentication successful with correct credentials")
        print(f"   User: {user.username} ({user.full_name})")
    else:
        print("❌ Authentication failed with correct credentials")
        return False

    # Test wrong password
    user = authenticate_user(fake_users_db, "johndoe", "wrongpassword")
    if not user:
        print("✅ Authentication correctly rejected wrong password")
    else:
        print("❌ Authentication incorrectly accepted wrong password")
        return False

    # Test wrong username
    user = authenticate_user(fake_users_db, "wronguser", "secret")
    if not user:
        print("✅ Authentication correctly rejected wrong username")
    else:
        print("❌ Authentication incorrectly accepted wrong username")
        return False

    print("\n🎉 All authentication tests passed!")
    return True


if __name__ == "__main__":
    test_authentication()
