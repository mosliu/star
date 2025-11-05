"""Database initialization script"""
from sqlalchemy import create_engine
from app.core.config import settings
from app.core.database import Base
from app.models import Child, StarRecord, Reward
from loguru import logger

def init_database():
    """Initialize database with tables"""
    logger.info("Initializing database...")
    
    # Create engine
    engine = create_engine(settings.database_url)
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    logger.info("Database tables created successfully")

if __name__ == "__main__":
    from app.core.logging import setup_logging
    setup_logging()
    init_database()
