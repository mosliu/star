from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import uvicorn
from loguru import logger
from pathlib import Path

from app.core.config import settings
from app.core.logging import setup_logging
from app.api.endpoints import children, stars, rewards


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    logger.info(f"Server running on {settings.host}:{settings.port}")
    logger.info(f"Debug mode: {settings.debug}")
    yield
    # Shutdown
    logger.info("Shutting down application")


# Setup logging
setup_logging()

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
    debug=settings.debug
)

# Custom exception handler for validation errors with binary data
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors, especially those containing binary data and file uploads"""
    from fastapi import UploadFile
    
    errors = []
    for error in exc.errors():
        # Create a safe error dict that handles binary data and non-serializable objects
        safe_error = {}
        for key, value in error.items():
            try:
                # Handle different value types
                if isinstance(value, bytes):
                    # For bytes, try to decode as UTF-8, or represent as hex
                    try:
                        safe_error[key] = value.decode('utf-8')
                    except UnicodeDecodeError:
                        # If it's not valid UTF-8, show it as hex string
                        safe_error[key] = f"<binary data: {value[:50].hex()}...>" if len(value) > 50 else f"<binary data: {value.hex()}>"
                elif isinstance(value, UploadFile):
                    # For UploadFile objects, provide a readable representation
                    safe_error[key] = f"<uploaded file: {value.filename} ({value.content_type})>"
                elif hasattr(value, '__dict__'):
                    # For objects with __dict__, try to extract relevant info
                    safe_error[key] = str(value)
                else:
                    safe_error[key] = value
            except Exception as e:
                # If any error occurs, provide a safe representation
                safe_error[key] = f"<{type(value).__name__} object>"
        errors.append(safe_error)
    
    return JSONResponse(
        status_code=422,
        content={"detail": errors}
    )

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for serving uploaded files (like Laravel's public/storage)
public_storage_path = Path("public/storage")
public_storage_path.mkdir(parents=True, exist_ok=True)

# Create subdirectories for uploads
avatars_path = public_storage_path / "avatars"
avatars_path.mkdir(parents=True, exist_ok=True)
rewards_path = public_storage_path / "rewards"
rewards_path.mkdir(parents=True, exist_ok=True)

app.mount("/storage", StaticFiles(directory="public/storage"), name="storage")

# Include routers
app.include_router(children.router, prefix="/api/children", tags=["children"])
app.include_router(stars.router, prefix="/api", tags=["stars"])
app.include_router(rewards.router, prefix="/api/rewards", tags=["rewards"])

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.app_version,
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    # Configure uvicorn logging to use loguru
    import logging
    import sys
    
    # Intercept uvicorn logs
    class InterceptHandler(logging.Handler):
        def emit(self, record):
            # Get corresponding Loguru level if it exists
            try:
                level = logger.level(record.levelname).name
            except ValueError:
                level = record.levelno
            
            # Find caller from where originated the logged message
            frame, depth = logging.currentframe(), 2
            while frame.f_code.co_filename == logging.__file__:
                frame = frame.f_back
                depth += 1
            
            logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())
    
    # Remove existing handlers and add our interceptor
    logging.getLogger("uvicorn").handlers = [InterceptHandler()]
    logging.getLogger("uvicorn.access").handlers = [InterceptHandler()]
    logging.getLogger("uvicorn.error").handlers = [InterceptHandler()]
    
    # Run with uvicorn
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        log_config=None  # Disable uvicorn's default logging config
    )
