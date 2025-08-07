from flask import Flask, request, jsonify
from ultralytics import YOLO
import cv2
import numpy as np
import requests
import os
import traceback
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Global variable to store the model
model = None

def load_model():
    """Load YOLOv8 model with error handling"""
    global model
    try:
        logger.info("Loading YOLOv8 model...")
        model = YOLO("yolov8n.pt")
        logger.info("Model loaded successfully!")
        return True
    except Exception as e:
        logger.error(f"Failed to load model: {str(e)}")
        logger.error(traceback.format_exc())
        return False

# Initialize model on startup
model_loaded = load_model()

def read_image_from_url(url):
    try:
        logger.info(f"Reading image from URL: {url}")
        resp = requests.get(url, stream=True, timeout=10)
        resp.raise_for_status()
        image = np.asarray(bytearray(resp.read()), dtype="uint8")
        result = cv2.imdecode(image, cv2.IMREAD_COLOR)
        if result is None:
            raise ValueError("Failed to decode image")
        logger.info("Image loaded successfully from URL")
        return result
    except Exception as e:
        logger.error(f"Failed to read image from URL: {str(e)}")
        raise

def read_image_from_file(file):
    try:
        logger.info("Reading image from file")
        npimg = np.frombuffer(file.read(), np.uint8)
        result = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
        if result is None:
            raise ValueError("Failed to decode uploaded image")
        logger.info("Image loaded successfully from file")
        return result
    except Exception as e:
        logger.error(f"Failed to read image from file: {str(e)}")
        raise

def predict_objects(image):
    try:
        logger.info("Starting object prediction")
        if model is None:
            raise RuntimeError("Model not loaded")
            
        results = model.predict(source=image)
        json_output = []

        for result in results:
            if result.boxes is not None:
                for box in result.boxes:
                    class_id = int(box.cls[0])
                    conf = float(box.conf[0])
                    xyxy = box.xyxy[0].tolist()

                    json_output.append({
                        "class_id": class_id,
                        "class_name": model.names[class_id],
                        "confidence": round(conf, 3),
                        "bbox": {
                            "x1": round(xyxy[0], 2),
                            "y1": round(xyxy[1], 2),
                            "x2": round(xyxy[2], 2),
                            "y2": round(xyxy[3], 2)
                        }
                    })
        
        logger.info(f"Prediction completed. Found {len(json_output)} objects")
        return json_output
    except Exception as e:
        logger.error(f"Failed to predict objects: {str(e)}")
        logger.error(traceback.format_exc())
        raise

@app.route("/", methods=["GET"])
def health_check():
    return jsonify({
        "status": "ok",
        "message": "YOLO Object Detection API",
        "model_loaded": model is not None
    })

@app.route("/predict", methods=["POST"])
def predict():
    try:
        logger.info("Received prediction request")
        
        if not model_loaded or model is None:
            return jsonify({"error": "Model not loaded. Please try again later."}), 503
        
        image = None
        
        if "file" in request.files:
            logger.info("Processing file upload")
            file = request.files["file"]
            if file.filename == '':
                return jsonify({"error": "No file selected"}), 400
            image = read_image_from_file(file)
        elif request.is_json and "url" in request.json:
            logger.info("Processing URL request")
            image_url = request.json["url"]
            if not image_url:
                return jsonify({"error": "URL is empty"}), 400
            image = read_image_from_url(image_url)
        else:
            return jsonify({"error": "No image provided. Send 'file' or 'url'."}), 400

        detections = predict_objects(image)
        logger.info(f"Returning {len(detections)} detections")
        return jsonify(detections)
        
    except Exception as e:
        logger.error(f"Error in predict endpoint: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
