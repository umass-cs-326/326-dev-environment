# test_api.py
import json
from typing import Optional

import requests


def print_request_details(response: requests.Response) -> None:
    """Print raw HTTP request details."""
    print("=== RAW HTTP REQUEST ===")
    request = response.request
    print(f"{request.method} {request.url}")

    # Print headers
    for name, value in request.headers.items():
        print(f"{name}: {value}")

    # Print body if present
    if request.body:
        print(f"\nRequest Body: {request.body}")
    print()


def print_response_details(response: requests.Response) -> None:
    """Print raw HTTP response details."""
    print("=== RAW HTTP RESPONSE ===")
    print(f"HTTP/1.1 {response.status_code} {response.reason}")

    # Print headers
    for name, value in response.headers.items():
        print(f"{name}: {value}")

    print(f"\nResponse Body: {response.text}")
    print("=" * 50)
    print()


def test_login() -> Optional[str]:
    """Test the login endpoint which sets a session cookie."""
    print("🔐 Testing Login Endpoint")
    response = requests.post(
        "http://127.0.0.1:8000/login",
        params={"username": "testuser"}
    )

    print_request_details(response)
    print_response_details(response)

    print("Login response (formatted):")
    print(json.dumps(response.json(), indent=2))

    # Extract session_id from cookies for next test
    session_id = response.cookies.get("session_id")
    print(f"Session ID from cookie: {session_id}")
    return session_id


def test_get_preferences(session_id: Optional[str] = None) -> None:
    """Test getting user preferences with session cookie."""
    print("📋 Testing Get Preferences Endpoint")
    cookies: dict[str, str] = {}
    if session_id:
        cookies["session_id"] = session_id

    response = requests.get(
        "http://127.0.0.1:8000/preferences",
        cookies=cookies
    )

    print_request_details(response)
    print_response_details(response)

    print("Preferences response (formatted):")
    if response.status_code == 200:
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Error {response.status_code}: {response.text}")


def test_get_preferences_without_session() -> None:
    """Test getting preferences without a valid session (should fail)."""
    print("❌ Testing preferences without session:")
    test_get_preferences()


if __name__ == "__main__":
    print("🚀 Starting Cookie API Tests\n")

    # Test login and get session ID
    session_id = test_login()
    print("\n" + "="*60 + "\n")

    # Test getting preferences with valid session
    print("✅ Testing preferences with valid session:")
    test_get_preferences(session_id)
    print("\n" + "="*60 + "\n")

    # Test getting preferences without session
    test_get_preferences_without_session()
