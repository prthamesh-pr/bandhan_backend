#!/usr/bin/env python3
"""
Test the deployed API with correct endpoints
"""

import requests
import time

def test_deployed_api():
    """Test the deployed API with the correct endpoints"""
    
    base_url = "https://bandhan-backend.onrender.com"
    
    print("🚀 Testing deployed YOLO API...")
    print("=" * 50)
    
    # Test health check at root
    print("🏥 Testing health check at root (/)...")
    try:
        response = requests.get(base_url, timeout=15)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Health check passed!")
            print(f"   Status: {result.get('status')}")
            print(f"   Model loaded: {result.get('model_loaded')}")
        else:
            print(f"❌ Health check failed: {response.text[:200]}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
    
    print()
    
    # Test predict endpoint with longer timeout
    print("🧪 Testing predict endpoint...")
    print("⏳ This may take up to 2 minutes for cold start...")
    
    data = {
        'url': 'https://images.unsplash.com/photo-1568702846914-96b305d2aaeb'
    }
    
    try:
        start_time = time.time()
        response = requests.post(f"{base_url}/predict", json=data, timeout=120)  # 2 minute timeout
        end_time = time.time()
        
        print(f"📊 Status: {response.status_code}")
        print(f"⏱️  Time taken: {end_time - start_time:.1f} seconds")
        
        if response.status_code == 200:
            try:
                result = response.json()
                print("✅ Success! Detections:")
                
                if result:
                    for i, detection in enumerate(result[:5]):  # Show first 5
                        class_name = detection.get('class_name', 'Unknown')
                        confidence = detection.get('confidence', 0)
                        print(f"   {i+1}. {class_name}: {confidence:.1%}")
                else:
                    print("   No objects detected")
                    
            except Exception as e:
                print(f"❌ Failed to parse response: {e}")
                print("Raw response:", response.text[:300])
        else:
            print(f"❌ Request failed")
            print("Response:", response.text[:500])
            
    except requests.exceptions.Timeout:
        print("⏰ Request timed out after 2 minutes")
        print("💡 The free tier may be too slow for YOLO processing")
    except Exception as e:
        print(f"🚫 Request failed: {e}")

if __name__ == "__main__":
    test_deployed_api()
