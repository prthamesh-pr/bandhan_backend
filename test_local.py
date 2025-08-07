#!/usr/bin/env python3
"""
Test local Flask app
"""

import requests

def test_local():
    """Test the local Flask app"""
    
    print("🧪 Testing local Flask app...")
    
    # Test health check
    try:
        response = requests.get("http://127.0.0.1:5000/", timeout=5)
        print(f"Health check: {response.status_code}")
        if response.status_code == 200:
            print("✅ Local app working!")
            result = response.json()
            print(f"   Status: {result.get('status')}")
            print(f"   Message: {result.get('message')}")
        else:
            print(f"❌ Health check failed: {response.text}")
    except Exception as e:
        print(f"❌ Failed to connect locally: {e}")

if __name__ == "__main__":
    test_local()
