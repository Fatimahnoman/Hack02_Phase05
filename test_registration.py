#!/usr/bin/env python3
"""
Test script to verify the registration endpoint works correctly.
"""
import requests
import json

def test_registration():
    """Test the registration endpoint"""
    print("Testing registration endpoint...")

    # Test data
    test_user = {
        "email": "testuser@example.com",
        "password": "testpassword123"
    }

    # Make request to registration endpoint
    try:
        response = requests.post("http://localhost:8001/api/auth/register", json=test_user)

        if response.status_code == 200:
            print("[SUCCESS] Registration successful!")
            user_data = response.json()
            print(f"User created: {user_data}")
        elif response.status_code == 400:
            print("[WARNING] Registration failed - user might already exist")
            print(f"Response: {response.json()}")
        else:
            print(f"[ERROR] Registration failed with status code: {response.status_code}")
            print(f"Response: {response.text}")

    except requests.exceptions.ConnectionError:
        print("[ERROR] Cannot connect to server. Make sure the backend is running on http://localhost:8001")
    except Exception as e:
        print(f"[ERROR] Error during registration test: {e}")

def test_login():
    """Test the login endpoint"""
    print("\nTesting login endpoint...")

    # Test data
    login_data = {
        "email": "testuser@example.com",
        "password": "testpassword123"
    }

    # Make request to login endpoint
    try:
        response = requests.post("http://localhost:8001/api/auth/login", json=login_data)

        if response.status_code == 200:
            print("[SUCCESS] Login successful!")
            token_data = response.json()
            print(f"Access token received: {'access_token' in token_data}")
        elif response.status_code == 401:
            print("[ERROR] Login failed - incorrect credentials")
            print(f"Response: {response.json()}")
        else:
            print(f"[ERROR] Login failed with status code: {response.status_code}")
            print(f"Response: {response.text}")

    except requests.exceptions.ConnectionError:
        print("[ERROR] Cannot connect to server. Make sure the backend is running on http://localhost:8001")
    except Exception as e:
        print(f"[ERROR] Error during login test: {e}")

if __name__ == "__main__":
    print("Testing registration and login endpoints...\n")
    test_registration()
    test_login()
    print("\nTest completed!")