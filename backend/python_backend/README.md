# Star Reward System API

A FastAPI-based backend for managing children's star rewards system.

## Features

- Children management (CRUD operations)
- Star points system (add/subtract stars)
- Rewards management and redemption
- Comprehensive logging with Loguru
- MySQL database support

## Installation

### Using uv (recommended)

```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh  # Unix/Linux/macOS
# or
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"  # Windows

# Install dependencies
uv pip install -r requirements.txt
```

### Using pip

```bash
pip install -r requirements.txt
```

## Configuration

1. Copy `.env.example` to `.env`
2. Update database connection and other settings in `.env`

## Database Setup

```bash
# Initialize database tables
python init_db.py

# Or use Alembic for migrations
alembic upgrade head
```

## Running the Application

### Windows
```bash
start.bat
```

### Unix/Linux/macOS
```bash
chmod +x start.sh
./start.sh
```

### Direct Python
```bash
python main.py
```

### Using uv
```bash
uv run python main.py
```

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Docker Support

```bash
# Build and run with docker-compose
docker-compose up --build
```

## Logging

Logs are stored in the `logs/` directory:
- `app_YYYY-MM-DD.log` - All application logs
- `errors_YYYY-MM-DD.log` - Error logs only

Logs are also output to console with color formatting.
