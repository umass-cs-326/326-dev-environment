import json
from pprint import pprint

import requests

# API endpoint
BASE_URL = "http://localhost:8000"


def pretty_print_response(response):
    """Print the status code and response in a readable format"""
    print(f"Status code: {response.status_code}")
    try:
        pprint(response.json())
    except:
        print(response.text)
    print()


def get_token(username, password):
    """Get authentication token"""
    response = requests.post(
        f"{BASE_URL}/token",
        data={"username": username, "password": password}
    )
    return response


def get_user_info(token):
    """Get current user information"""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/users/me", headers=headers)
    return response


def get_user_items(token):
    """Get items belonging to the authenticated user"""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/users/me/items/", headers=headers)
    return response


def access_without_token():
    """Attempt to access protected endpoint without a token"""
    response = requests.get(f"{BASE_URL}/users/me")
    return response


def main():
    print("=== Authentication Demo ===")

    # Test successful authentication flow
    print("Attempting to get token...")
    response = get_token("johndoe", "secret")
    pretty_print_response(response)

    if response.status_code == 200:
        token_data = response.json()
        token = token_data["access_token"]

        print("Fetching user information...")
        user_response = get_user_info(token)
        pretty_print_response(user_response)

        print("Fetching user's items...")
        items_response = get_user_items(token)
        pretty_print_response(items_response)

    # Test invalid credentials
    print("=== Testing Invalid Authentication ===")
    print("Attempting to get token...")
    invalid_response = get_token("johndoe", "wrongpassword")
    pretty_print_response(invalid_response)

    if invalid_response.status_code == 401:
        print("Authentication failed as expected")

    # Test missing token
    print("=== Testing Missing Token ===")
    print("Attempting to access protected endpoint without token...")
    missing_token_response = access_without_token()
    pretty_print_response(missing_token_response)


if __name__ == "__main__":
    main()
