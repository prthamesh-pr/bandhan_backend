import requests
import json

def test_deployed_api():
    """
    Test the deployed Flask API on Render with an apple image
    """
    
    # Your deployed API endpoint
    url = "https://bandhan-backend.onrender.com/predict"
    
    # Using a publicly available apple image URL for testing
    test_data = {
        "url": "https://images.unsplash.com/photo-1568702846914-96b305d2aaeb?w=500"
    }
    
    print("🔍 Testing YOLO Object Detection API")
    print(f"🌐 API Endpoint: {url}")
    print("🍎 Analyzing apple image...")
    print("=" * 60)
    
    try:
        # Send request to your deployed API
        response = requests.post(url, json=test_data, timeout=30)
        
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
                    
                    # Calculate dimensions
                    width = detection['bbox']['x2'] - detection['bbox']['x1']
                    height = detection['bbox']['y2'] - detection['bbox']['y1']
                    print(f"   📏 Size: {width:.1f} x {height:.1f} pixels")
                    print()
                    
                print(f"🎉 Total objects detected: {len(detections)}")
            else:
                print("❌ No objects detected in the image.")
                
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.Timeout:
        print("⏰ Error: Request timed out. The API might be starting up (cold start).")
        print("💡 Try again in a few seconds.")
    except requests.exceptions.ConnectionError:
        print("🔌 Error: Could not connect to the API.")
        print("💡 Check if the deployment is running properly.")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def test_with_file_upload():
    """
    Test file upload to the deployed API (if apple.jpg exists locally)
    """
    
    url = "https://bandhan-backend.onrender.com/predict"
    
    try:
        # Check if local apple image exists
        with open("apple.jpg", "rb") as f:
            files = {"file": f}
            print("\n🔍 Testing with file upload...")
            response = requests.post(url, files=files, timeout=30)
            
            if response.status_code == 200:
                detections = response.json()
                print("✅ File upload test: SUCCESS")
                print(f"🎉 Detected {len(detections)} objects")
            else:
                print(f"❌ File upload error: {response.status_code}")
                
    except FileNotFoundError:
        print("\n💡 Skipping file upload test (apple.jpg not found)")
    except Exception as e:
        print(f"\n❌ File upload error: {e}")

if __name__ == "__main__":
    test_deployed_api()
    test_with_file_upload()
