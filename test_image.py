import requests
import json
from PIL import Image
import io
import base64

def test_image_detection():
    # The image you provided (apple image)
    # Since we can't directly access the attachment, we'll use a publicly available apple image URL
    # or you can save the image locally and modify the path
    
    # For demonstration, let's use a direct approach with the local Flask server
    url = "http://127.0.0.1:5000/predict"
    
    # You can either:
    # 1. Save the attached image and use file upload
    # 2. Use a URL to a similar apple image
    
    # Method 1: Using a URL (example with a publicly available apple image)
    test_data = {
        "url": "https://images.unsplash.com/photo-1568702846914-96b305d2aaeb?w=500"
    }
    
    try:
        response = requests.post(url, json=test_data)
        if response.status_code == 200:
            detections = response.json()
            print("Object Detection Results:")
            print("=" * 40)
            
            if detections:
                for i, detection in enumerate(detections, 1):
                    print(f"Detection {i}:")
                    print(f"  Class: {detection['class_name']} (ID: {detection['class_id']})")
                    print(f"  Confidence: {detection['confidence']}")
                    print(f"  Bounding Box: x1={detection['bbox']['x1']}, y1={detection['bbox']['y1']}, x2={detection['bbox']['x2']}, y2={detection['bbox']['y2']}")
                    print()
            else:
                print("No objects detected in the image.")
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the Flask server. Make sure it's running on http://127.0.0.1:5000")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_image_detection()
