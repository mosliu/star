"""Quick server test"""
import subprocess
import time
import requests
from loguru import logger

def test_server():
    """Start server and test endpoints"""
    logger.info("Starting FastAPI server...")
    
    # Start server in background
    process = subprocess.Popen(
        ["python", "main.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait for server to start
    time.sleep(5)
    
    try:
        # Test root endpoint
        response = requests.get("http://localhost:8000/")
        logger.info(f"Root endpoint: {response.status_code}")
        
        # Test health endpoint
        response = requests.get("http://localhost:8000/health")
        logger.info(f"Health endpoint: {response.status_code}")
        
        # Test docs
        response = requests.get("http://localhost:8000/docs")
        logger.info(f"Docs endpoint: {response.status_code}")
        
        logger.success("Server is running successfully!")
        logger.info("Visit http://localhost:8000/docs for API documentation")
        
    except requests.exceptions.ConnectionError:
        logger.error("Could not connect to server. Please check if it's running.")
    finally:
        # Stop server
        process.terminate()
        process.wait()

if __name__ == "__main__":
    test_server()
