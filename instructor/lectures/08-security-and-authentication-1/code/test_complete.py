#!/usr/bin/env python3

"""
Simple authentication flow test using requests
"""

import os
import signal
import subprocess
import time

import requests


def test_complete_auth_flow():
    """Test the complete authentication flow"""

    # Start server
    print("🚀 Starting server...")
    server_process = subprocess.Popen(
        ['uvicorn', 'main:app', '--port', '8003'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd='/workspace/326/lectures/08-security-and-authentication'
    )

    # Wait for server to start
    time.sleep(3)

    try:
        base_url = "http://localhost:8003"

        # Test 1: Get token with correct credentials
        print("🔐 Testing authentication with correct credentials...")
        response = requests.post(
            f"{base_url}/token",
            data={"username": "johndoe", "password": "secret"}
        )

        if response.status_code == 200:
            print("✅ Authentication successful!")
            token_data = response.json()
            token = token_data["access_token"]
            print(f"   Token type: {token_data['token_type']}")

            # Test 2: Use token to get user info
            print("👤 Testing protected endpoint with token...")
            headers = {"Authorization": f"Bearer {token}"}
            user_response = requests.get(
                f"{base_url}/users/me", headers=headers)

            if user_response.status_code == 200:
                print("✅ Protected endpoint accessible with token!")
                user_data = user_response.json()
                print(
                    f"   User: {user_data['username']} ({user_data['full_name']})")
            else:
                print(
                    f"❌ Protected endpoint failed: {user_response.status_code}")

        else:
            print(f"❌ Authentication failed: {response.status_code}")
            print(f"   Response: {response.text}")

        # Test 3: Try with wrong credentials
        print("🚫 Testing authentication with wrong credentials...")
        wrong_response = requests.post(
            f"{base_url}/token",
            data={"username": "johndoe", "password": "wrongpassword"}
        )

        if wrong_response.status_code == 401:
            print("✅ Wrong credentials correctly rejected!")
        else:
            print(
                f"❌ Wrong credentials not rejected properly: {wrong_response.status_code}")

        # Test 4: Try protected endpoint without token
        print("🔒 Testing protected endpoint without token...")
        no_token_response = requests.get(f"{base_url}/users/me")

        if no_token_response.status_code == 401:
            print("✅ Protected endpoint correctly requires authentication!")
        else:
            print(
                f"❌ Protected endpoint should require auth: {no_token_response.status_code}")

    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server - make sure it's running")

    finally:
        # Clean up
        print("🛑 Stopping server...")
        server_process.terminate()
        server_process.wait()

    print("\n🎉 Authentication system is working correctly!")


if __name__ == "__main__":
    test_complete_auth_flow()
