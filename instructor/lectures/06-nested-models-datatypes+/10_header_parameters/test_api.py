# test_api.py
import json

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


def test_valid_headers() -> None:
    """Test the API with valid headers."""
    print("✅ Testing with valid headers")

    headers = {
        "User-Agent": "Mozilla/5.0 (Python-requests/2.31.0)",
        "X-Token": "fake-super-secret-token"
    }

    response = requests.get(
        "http://127.0.0.1:8000/items/",
        headers=headers
    )

    print_request_details(response)
    print_response_details(response)

    print("Response (formatted):")
    if response.status_code == 200:
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Error {response.status_code}: {response.text}")


def test_invalid_token() -> None:
    """Test the API with invalid X-Token header."""
    print("❌ Testing with invalid X-Token header")

    headers = {
        "User-Agent": "Mozilla/5.0 (Python-requests/2.31.0)",
        "X-Token": "invalid-token"
    }

    response = requests.get(
        "http://127.0.0.1:8000/items/",
        headers=headers
    )

    print_request_details(response)
    print_response_details(response)

    print("Response (formatted):")
    if response.status_code == 200:
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Error {response.status_code}: {response.text}")


def test_missing_token() -> None:
    """Test the API without X-Token header."""
    print("⚠️  Testing without X-Token header")

    headers = {
        "User-Agent": "Mozilla/5.0 (Python-requests/2.31.0)"
    }

    response = requests.get(
        "http://127.0.0.1:8000/items/",
        headers=headers
    )

    print_request_details(response)
    print_response_details(response)

    print("Response (formatted):")
    if response.status_code == 200:
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Error {response.status_code}: {response.text}")


def test_no_custom_headers() -> None:
    """Test the API with no custom headers (only default requests headers)."""
    print("🔍 Testing with no custom headers")

    response = requests.get("http://127.0.0.1:8000/items/")

    print_request_details(response)
    print_response_details(response)

    print("Response (formatted):")
    if response.status_code == 200:
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Error {response.status_code}: {response.text}")


def test_custom_user_agent() -> None:
    """Test the API with a custom User-Agent."""
    print("🤖 Testing with custom User-Agent")

    headers = {
        "User-Agent": "MyCustomApp/1.0 (Testing API)",
        "X-Token": "fake-super-secret-token"
    }

    response = requests.get(
        "http://127.0.0.1:8000/items/",
        headers=headers
    )

    print_request_details(response)
    print_response_details(response)

    print("Response (formatted):")
    if response.status_code == 200:
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Error {response.status_code}: {response.text}")


if __name__ == "__main__":
    print("🚀 Starting Header Parameters API Tests\n")

    # Test with valid headers
    test_valid_headers()
    print("\n" + "="*60 + "\n")

    # Test with invalid token
    test_invalid_token()
    print("\n" + "="*60 + "\n")

    # Test without token
    test_missing_token()
    print("\n" + "="*60 + "\n")

    # Test with no custom headers
    test_no_custom_headers()
    print("\n" + "="*60 + "\n")

    # Test with custom User-Agent
    test_custom_user_agent()
