import requests
import json
from pathlib import Path

def test_with_local_image():
    """
    Test the Flask API with a local image file
    Save your apple image as 'apple.jpg' in this directory and run this script
    """
    
    url = "http://127.0.0.1:5000/predict"
    
    # Check if apple image exists
    image_path = Path("apple.jpg")
    if not image_path.exists():
        print("Please save your apple image as 'apple.jpg' in the current directory")
        print("Then run this script again.")
        return
    
    try:
        # Send image file to the Flask API
        with open(image_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(url, files=files)
        
        if response.status_code == 200:
            detections = response.json()
            print("🍎 Apple Image Analysis Results:")
            print("=" * 50)
            
            if detections:
                for i, detection in enumerate(detections, 1):
                    print(f"📍 Detection {i}:")
                    print(f"   Object: {detection['class_name']} (Class ID: {detection['class_id']})")
                    print(f"   Confidence: {detection['confidence'] * 100:.1f}%")
                    print(f"   Location: x1={detection['bbox']['x1']:.1f}, y1={detection['bbox']['y1']:.1f}")
                    print(f"            x2={detection['bbox']['x2']:.1f}, y2={detection['bbox']['y2']:.1f}")
                    
                    # Calculate dimensions
                    width = detection['bbox']['x2'] - detection['bbox']['x1']
                    height = detection['bbox']['y2'] - detection['bbox']['y1']
                    print(f"   Size: {width:.1f} x {height:.1f} pixels")
                    print()
                    
                print(f"✅ Total objects detected: {len(detections)}")
            else:
                print("❌ No objects detected in the image.")
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the Flask server.")
        print("Make sure the Flask app is running on http://127.0.0.1:5000")
    except FileNotFoundError:
        print("❌ Error: Could not find the image file.")
    except Exception as e:
        print(f"❌ Error: {e}")

def show_instructions():
    print("🔍 YOLO Object Detection Test")
    print("=" * 30)
    print("Your Flask application is running and ready!")
    print()
    print("To test with your apple image:")
    print("1. Save the apple image as 'apple.jpg' in this directory")
    print("2. Run: python test_local_image.py")
    print()
    print("Or use the API directly:")
    print("POST http://127.0.0.1:5000/predict")
    print("- Send image file: multipart/form-data with 'file' field")
    print("- Send image URL: JSON with 'url' field")
    print()

if __name__ == "__main__":
    show_instructions()
    test_with_local_image()
