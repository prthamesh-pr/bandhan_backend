from flask import Flask, request, jsonify
import os
import logging
import traceback

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Global variable to store the model (lazy loading)
model = None
model_loading_error = None

def load_model():
    """Load YOLOv8 model with comprehensive error handling"""
    global model, model_loading_error
    
    if model is not None:
        return True
    
    try:
        logger.info("Starting YOLOv8 model loading...")
        
        # Import ultralytics only when needed
        from ultralytics import YOLO
        import cv2
        import numpy as np
        
        logger.info("Dependencies imported successfully")
        logger.info("Loading YOLOv8n model...")
        
        model = YOLO("yolov8n.pt")
        logger.info("✅ Model loaded successfully!")
        return True
        
    except Exception as e:
        error_msg = f"Failed to load YOLO model: {str(e)}"
        logger.error(error_msg)
        logger.error(traceback.format_exc())
        model_loading_error = error_msg
        return False

def read_image_from_url(url):
    """Download and decode image from URL"""
    try:
        import requests
        import cv2
        import numpy as np
        
        logger.info(f"Downloading image from: {url}")
        response = requests.get(url, stream=True, timeout=15)
        response.raise_for_status()
        
        # Convert to numpy array and decode
        image_array = np.asarray(bytearray(response.content), dtype="uint8")
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        
        if image is None:
            raise ValueError("Failed to decode image")
            
        logger.info("✅ Image loaded successfully")
        return image
        
    except Exception as e:
        logger.error(f"Failed to load image: {str(e)}")
        raise

def predict_objects(image):
    """Run YOLO prediction on image"""
    try:
        logger.info("Running YOLO prediction...")
        results = model.predict(source=image, verbose=False)
        
        detections = []
        for result in results:
            if result.boxes is not None:
                for box in result.boxes:
                    class_id = int(box.cls[0])
                    confidence = float(box.conf[0])
                    bbox = box.xyxy[0].tolist()
                    
                    detections.append({
                        "class_id": class_id,
                        "class_name": model.names[class_id],
                        "confidence": round(confidence, 3),
                        "bbox": {
                            "x1": round(bbox[0], 2),
                            "y1": round(bbox[1], 2),
                            "x2": round(bbox[2], 2),
                            "y2": round(bbox[3], 2)
                        }
                    })
        
        logger.info(f"✅ Found {len(detections)} objects")
        return detections
        
    except Exception as e:
        logger.error(f"Prediction failed: {str(e)}")
        raise

@app.route("/", methods=["GET"])
def health_check():
    """Health check endpoint"""
    try:
        status = {
            "status": "healthy",
            "service": "YOLO Object Detection API",
            "python_version": os.sys.version.split()[0],
        }
        
        # Check if model can be loaded (but don't actually load it unless needed)
        if model is not None:
            status["model_status"] = "loaded"
        elif model_loading_error:
            status["model_status"] = "failed"
            status["model_error"] = model_loading_error
        else:
            status["model_status"] = "not_loaded"
            
        return jsonify(status)
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/predict", methods=["POST"])
def predict():
    """Object detection endpoint"""
    try:
        logger.info("🔍 Received prediction request")
        
        # Validate request
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400
            
        data = request.get_json()
        if not data or "url" not in data:
            return jsonify({"error": "Missing 'url' field in request"}), 400
            
        image_url = data["url"]
        if not image_url:
            return jsonify({"error": "URL cannot be empty"}), 400
        
        logger.info(f"Processing image URL: {image_url}")
        
        # Try to load model if not already loaded
        if not load_model():
            return jsonify({
                "error": "YOLO model failed to load", 
                "details": model_loading_error
            }), 503
        
        # Download and process image
        image = read_image_from_url(image_url)
        detections = predict_objects(image)
        
        logger.info(f"✅ Returning {len(detections)} detections")
        return jsonify({
            "success": True,
            "detections": detections,
            "count": len(detections)
        })
        
    except Exception as e:
        error_msg = f"Prediction failed: {str(e)}"
        logger.error(error_msg)
        logger.error(traceback.format_exc())
        return jsonify({"error": error_msg}), 500

@app.route("/test", methods=["GET"])
def test():
    """Simple test endpoint"""
    return jsonify({
        "status": "ok", 
        "message": "API is responding",
        "endpoints": ["/", "/test", "/predict"]
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    logger.info(f"🚀 Starting Flask app on port {port}")
    app.run(host="0.0.0.0", port=port, debug=False)
