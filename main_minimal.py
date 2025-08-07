from flask import Flask, jsonify, request
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route("/", methods=["GET"])
def health_check():
    """Basic health check endpoint"""
    try:
        return jsonify({
            "status": "ok", 
            "message": "Flask app is running!",
            "python_version": os.sys.version,
            "port": os.environ.get("PORT", "5000")
        })
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/test", methods=["GET"])
def test_endpoint():
    """Test endpoint"""
    return jsonify({"message": "Test endpoint working!"})

@app.route("/predict", methods=["POST"])
def predict():
    """Minimal predict endpoint for testing"""
    try:
        logger.info("Received prediction request")
        
        # Just return a test response for now
        return jsonify({
            "status": "test_mode",
            "message": "This is a test response - YOLO model not loaded yet",
            "detections": []
        })
        
    except Exception as e:
        logger.error(f"Error in predict endpoint: {str(e)}")
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
