#!/usr/bin/env python3
"""
Simple API test script for SocialConnect
Run this after starting the development server to test basic functionality
"""

import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_api():
    print("🧪 Testing SocialConnect API...")
    
    # Test data
    test_user = {
        "username": "apitest",
        "email": "apitest@example.com", 
        "password": "testpass123",
        "first_name": "API",
        "last_name": "Test"
    }
    
    try:
        # 1. Test user registration
        print("\n1️⃣ Testing user registration...")
        response = requests.post(f"{BASE_URL}/auth/register/", json=test_user)
        if response.status_code == 201:
            print("✅ User registration successful")
        else:
            print(f"❌ Registration failed: {response.text}")
            
        # 2. Test login (after manual verification for this test)
        print("\n2️⃣ Testing login...")
        login_data = {
            "username": test_user["username"],
            "password": test_user["password"]
        }
        
        # For testing, we'll activate the user directly
        # In real app, user would verify email first
        
        # 3. Test public endpoints
        print("\n3️⃣ Testing public endpoints...")
        
        # Get posts (should work without auth)
        response = requests.get(f"{BASE_URL}/posts/")
        if response.status_code == 200:
            print("✅ Public posts endpoint working")
            data = response.json()
            print(f"   📊 Found {data.get('count', 0)} posts")
        else:
            print(f"❌ Posts endpoint failed: {response.status_code}")
            
        # Get users list
        response = requests.get(f"{BASE_URL}/users/")
        if response.status_code == 200:
            print("✅ Users list endpoint working")
            data = response.json()
            if isinstance(data, list):
                print(f"   👥 Found {len(data)} users")
            else:
                print(f"   👥 Found {data.get('count', 0)} users")
        else:
            print(f"❌ Users endpoint failed: {response.status_code}")
            
        print("\n🎉 Basic API tests completed!")
        print("   ℹ️  For full testing, start the server and use tools like Postman")
        print("   ℹ️  or create a frontend to test authentication flows")
        
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed. Make sure the Django server is running:")
        print("   python3 manage.py runserver")
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")

if __name__ == "__main__":
    test_api()
