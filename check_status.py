#!/usr/bin/env python3
"""
Quick API status check
"""

import requests

def check_api_status():
    """Check if the API is responding at all"""
    
    base_url = "https://bandhan-backend.onrender.com"
    
    # Test root endpoint
    print("🔍 Checking root endpoint...")
    try:
        response = requests.get(base_url, timeout=10)
        print(f"Root endpoint status: {response.status_code}")
        print(f"Response: {response.text[:200]}")
    except Exception as e:
        print(f"Root endpoint failed: {e}")
    
    print()
    
    # Test health endpoint
    print("🏥 Checking health endpoint...")
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        print(f"Health endpoint status: {response.status_code}")
        print(f"Response: {response.text[:200]}")
    except Exception as e:
        print(f"Health endpoint failed: {e}")

if __name__ == "__main__":
    check_api_status()
