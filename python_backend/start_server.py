"""Start server with database migration"""
import subprocess
import sys
from pathlib import Path
from loguru import logger

def main():
    """Start the server with all necessary setup"""
    logger.info("=" * 60)
    logger.info("Starting Star Reward System - Python Backend")
    logger.info("=" * 60)
    
    # Step 1: Run database migration
    logger.info("Step 1: Running database migration...")
    try:
        subprocess.run([sys.executable, "migrate_db.py"], check=True)
        logger.success("Database migration completed")
    except subprocess.CalledProcessError as e:
        logger.error(f"Database migration failed: {e}")
        sys.exit(1)
    
    # Step 2: Ensure upload directories exist
    logger.info("Step 2: Creating upload directories...")
    public_storage = Path("public/storage")
    (public_storage / "avatars").mkdir(parents=True, exist_ok=True)
    (public_storage / "rewards").mkdir(parents=True, exist_ok=True)
    logger.success("Upload directories ready")
    
    # Step 3: Start the server
    logger.info("Step 3: Starting FastAPI server...")
    logger.info("-" * 40)
    logger.info("Server will be available at:")
    logger.info("  API: http://localhost:8000")
    logger.info("  Docs: http://localhost:8000/docs")
    logger.info("-" * 40)
    
    try:
        subprocess.run([sys.executable, "main.py"], check=True)
    except KeyboardInterrupt:
        logger.info("\nServer stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    from app.core.logging import setup_logging
    setup_logging()
    main()
