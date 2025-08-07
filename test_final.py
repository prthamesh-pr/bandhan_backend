import requests
import time

def test_health_check():
    """
    Test the health check endpoint first
    """
    url = "https://bandhan-backend.onrender.com/"
    
    print("🏥 Testing health check endpoint...")
    
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            data = response.json()
            print("✅ Health check successful!")
            print(f"📊 Status: {data.get('status')}")
            print(f"📝 Message: {data.get('message')}")
            print(f"🤖 Model loaded: {data.get('model_loaded')}")
            return data.get('model_loaded', False)
        else:
            print(f"❌ Health check failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_prediction():
    """
    Test the prediction endpoint
    """
    url = "https://bandhan-backend.onrender.com/predict"
    
    # Test with the apple image
    test_data = {
        "url": "https://images.unsplash.com/photo-1568702846914-96b305d2aaeb?w=500"
    }
    
    print("\n🍎 Testing prediction with apple image...")
    
    try:
        response = requests.post(url, json=test_data, timeout=60)
        
        if response.status_code == 200:
            detections = response.json()
            print("✅ Prediction successful!")
            
            if detections:
                for i, detection in enumerate(detections, 1):
                    print(f"\n📍 Detection {i}:")
                    print(f"   🏷️  Object: {detection['class_name']} (ID: {detection['class_id']})")
                    print(f"   🎯 Confidence: {detection['confidence'] * 100:.1f}%")
                    print(f"   📐 Bounding Box: ({detection['bbox']['x1']:.1f}, {detection['bbox']['y1']:.1f}) to ({detection['bbox']['x2']:.1f}, {detection['bbox']['y2']:.1f})")
                    
                print(f"\n🎉 Total objects detected: {len(detections)}")
            else:
                print("❓ No objects detected in the image")
            return True
        else:
            print(f"❌ Prediction failed: {response.status_code}")
            try:
                error_data = response.json()
                print(f"Error: {error_data.get('error', 'Unknown error')}")
            except:
                print(f"Response: {response.text[:200]}...")
            return False
            
    except Exception as e:
        print(f"❌ Prediction error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Testing deployed YOLO API...")
    print("=" * 50)
    
    # Wait a moment for deployment
    print("⏳ Waiting for deployment to complete...")
    time.sleep(10)
    
    # Test health check first
    model_ready = test_health_check()
    
    if model_ready:
        # Test prediction
        test_prediction()
    else:
        print("\n❌ Model not ready or health check failed")
        print("💡 The application might still be deploying or there could be an issue")
        print("   Try running this test again in a few minutes")
