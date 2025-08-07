import requests
import time
import json

def test_api_with_retries():
    """
    Test the deployed API with retries for cold starts
    """
    
    url = "https://bandhan-backend.onrender.com/predict"
    
    # Simple test image URL
    test_data = {
        "url": "https://images.unsplash.com/photo-1568702846914-96b305d2aaeb?w=500"
    }
    
    max_retries = 3
    timeout = 60  # Increase timeout for cold starts
    
    print("🔍 Testing YOLO Object Detection API")
    print(f"🌐 API Endpoint: {url}")
    print("🍎 Testing with apple image...")
    print("=" * 60)
    
    for attempt in range(1, max_retries + 1):
        try:
            print(f"📡 Attempt {attempt}/{max_retries} - Sending request...")
            
            response = requests.post(url, json=test_data, timeout=timeout)
            
            if response.status_code == 200:
                detections = response.json()
                print("✅ API Response: SUCCESS")
                print("🎯 Detection Results:")
                print("=" * 40)
                
                if detections:
                    for i, detection in enumerate(detections, 1):
                        print(f"📍 Detection {i}:")
                        print(f"   🏷️  Object: {detection['class_name']} (ID: {detection['class_id']})")
                        print(f"   🎯 Confidence: {detection['confidence'] * 100:.1f}%")
                        print(f"   📐 Bounding Box:")
                        print(f"      Top-left: ({detection['bbox']['x1']:.1f}, {detection['bbox']['y1']:.1f})")
                        print(f"      Bottom-right: ({detection['bbox']['x2']:.1f}, {detection['bbox']['y2']:.1f})")
                        
                        width = detection['bbox']['x2'] - detection['bbox']['x1']
                        height = detection['bbox']['y2'] - detection['bbox']['y1']
                        print(f"   📏 Size: {width:.1f} x {height:.1f} pixels")
                        print()
                        
                    print(f"🎉 Total objects detected: {len(detections)}")
                    return True
                else:
                    print("❌ No objects detected in the image.")
                    return True
                    
            elif response.status_code == 502:
                print(f"🔄 Attempt {attempt}: Server is starting up (502 Bad Gateway)")
                if attempt < max_retries:
                    print(f"⏳ Waiting 30 seconds before retry...")
                    time.sleep(30)
                else:
                    print("❌ Server failed to start after multiple attempts")
                    print("💡 This might be due to:")
                    print("   - Cold start issues on Render's free tier")
                    print("   - Server configuration problems")
                    print("   - Resource limitations")
                    
            else:
                print(f"❌ API Error: {response.status_code}")
                print(f"Response: {response.text[:500]}...")
                break
                
        except requests.exceptions.Timeout:
            print(f"⏰ Attempt {attempt}: Request timed out")
            if attempt < max_retries:
                print(f"⏳ Waiting 15 seconds before retry...")
                time.sleep(15)
            else:
                print("❌ All attempts timed out")
                
        except requests.exceptions.ConnectionError:
            print(f"🔌 Attempt {attempt}: Connection error")
            if attempt < max_retries:
                print(f"⏳ Waiting 15 seconds before retry...")
                time.sleep(15)
            else:
                print("❌ Unable to connect after multiple attempts")
                
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            break
    
    return False

def check_server_status():
    """
    Check if the server is responding at all
    """
    try:
        response = requests.get("https://bandhan-backend.onrender.com", timeout=10)
        print(f"🌐 Server status check: {response.status_code}")
        if response.status_code == 404:
            print("✅ Server is running (404 expected for root path)")
        return True
    except Exception as e:
        print(f"❌ Server status check failed: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Checking server status first...")
    if check_server_status():
        print("\n" + "="*60)
        test_api_with_retries()
    else:
        print("\n❌ Server appears to be down. Check your Render deployment.")
