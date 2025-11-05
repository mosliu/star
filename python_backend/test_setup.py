"""Test script to verify the setup"""
import sys
from loguru import logger

def test_imports():
    """Test if all required modules can be imported"""
    try:
        import fastapi
        import uvicorn
        import loguru
        import pydantic
        import sqlalchemy
        logger.info("✓ All core packages imported successfully")
        return True
    except ImportError as e:
        logger.error(f"✗ Import error: {e}")
        return False

def test_app_import():
    """Test if the app can be imported"""
    try:
        from main import app
        logger.info("✓ FastAPI app imported successfully")
        return True
    except Exception as e:
        logger.error(f"✗ Error importing app: {e}")
        return False

def test_logging():
    """Test logging setup"""
    try:
        from app.core.logging import setup_logging
        setup_logging()
        logger.info("✓ Logging system initialized successfully")
        return True
    except Exception as e:
        logger.error(f"✗ Error setting up logging: {e}")
        return False

if __name__ == "__main__":
    logger.remove()
    logger.add(sys.stdout, colorize=True, format="<green>{time:HH:mm:ss}</green> | <level>{message}</level>")
    
    logger.info("Testing Star Reward System setup...")
    
    results = []
    results.append(test_imports())
    results.append(test_logging())
    results.append(test_app_import())
    
    if all(results):
        logger.success("✓ All tests passed! Setup is complete.")
        logger.info("You can now start the server with: python main.py")
    else:
        logger.error("✗ Some tests failed. Please check the errors above.")
        sys.exit(1)
