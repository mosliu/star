from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Application settings
    app_name: str = "Star Reward System API"
    app_version: str = "1.0.0"
    debug: bool = True
    
    # Server settings
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = True
    
    # Database settings
    database_url: str = "mysql+pymysql://root:password@localhost/star_db"
    
    # CORS settings
    cors_origins: list = ["http://localhost:3000", "http://localhost:5173"]
    
    # JWT settings
    secret_key: str = "your-secret-key-here-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # File upload settings
    upload_dir: str = "uploads"
    max_upload_size: int = 5 * 1024 * 1024  # 5MB
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
