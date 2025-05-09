from flask import Flask, jsonify
import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("HealthCheck")

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    logger.info("Health check endpoint accessed")
    return jsonify({
        "status": "healthy",
        "message": "Service is running correctly"
    }), 200

@app.route('/', methods=['GET'])
def root():
    logger.info("Root endpoint accessed")
    return jsonify({
        "status": "online",
        "service": "Telegram ID Bot",
        "health_check": "/health"
    }), 200

def run_health_server():
    port = int(os.environ.get("PORT", 8000))
    logger.info(f"Starting health check server on port {port}")
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    run_health_server()