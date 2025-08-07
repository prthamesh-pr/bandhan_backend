#!/usr/bin/env python3
"""
Basic test for deployed YOLO API
"""

import requests

def test_basic_predict():
    """Test the basic predict endpoint"""
    
    url = "https://bandhan-backend.onrender.com/predict"
    
    # Test with the apple image URL
    data = {
        'url': 'https://images.unsplash.com/photo-1568702846914-96b305d2aaeb'
    }
    
    print("🧪 Testing basic /predict endpoint...")
    print(f"📡 URL: {url}")
    print(f"🔗 Image URL: {data['url']}")
    print()
    
    try:
        response = requests.post(url, json=data, timeout=30)
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            try:
                result = response.json()
                print("✅ Success! Response:")
                print(f"   Detected objects: {len(result.get('detections', []))}")
                
                if result.get('detections'):
                    for i, detection in enumerate(result['detections'][:3]):  # Show first 3
                        print(f"   {i+1}. {detection.get('class', 'Unknown')}: {detection.get('confidence', 0):.1%}")
                
            except Exception as e:
                print(f"❌ Failed to parse JSON response: {e}")
                print("Raw response:", response.text[:200])
        
        else:
            print(f"❌ Request failed with status {response.status_code}")
            print("Response:", response.text[:500])
            
    except requests.exceptions.Timeout:
        print("⏰ Request timed out (30 seconds)")
    except requests.exceptions.RequestException as e:
        print(f"🚫 Request failed: {e}")

if __name__ == "__main__":
    test_basic_predict()
