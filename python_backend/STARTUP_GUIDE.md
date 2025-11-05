# Star Reward System - Startup Guide

## Quick Start (Windows)

1. **Install dependencies** (if not already done):
```bash
cd E:\workspace_python\star\backend\python_backend
uv pip install -r requirements.txt --system
```

2. **Configure database**:
   - Edit `.env` file with your MySQL connection details
   - Default: `mysql+pymysql://root:password@localhost/star_db`

3. **Initialize database** (optional, for new database):
```bash
python init_db.py
```

4. **Start the server**:
```bash
# Option 1: Using the batch script
start.bat

# Option 2: Using uv directly
uv run python main.py

# Option 3: Using Python directly
python main.py
```

## API Endpoints

Once the server is running on `http://localhost:8000`:

### Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Main Endpoints

#### Children Management
- `GET /api/children` - List all children
- `GET /api/children/{id}` - Get child details
- `POST /api/children` - Create new child
- `PATCH /api/children/{id}` - Update child
- `DELETE /api/children/{id}` - Delete child

#### Star Operations
- `POST /api/children/{id}/stars/add` - Add stars to a child
- `POST /api/children/{id}/stars/subtract` - Subtract stars from a child

#### Rewards Management
- `GET /api/rewards` - List all rewards
- `GET /api/rewards/{id}` - Get reward details
- `POST /api/rewards` - Create new reward
- `PATCH /api/rewards/{id}` - Update reward
- `DELETE /api/rewards/{id}` - Delete reward
- `POST /api/rewards/{id}/redeem` - Redeem a reward

## Features

1. **Logging System**:
   - Console output with colors
   - Daily rotating log files in `logs/` directory
   - Separate error log files

2. **Database**:
   - MySQL support via SQLAlchemy
   - Automatic table creation
   - Migration support with Alembic

3. **Development Features**:
   - Hot reload in development mode
   - Debug logging
   - CORS enabled for frontend development

## Troubleshooting

### Port Already in Use
Change the port in `.env` file:
```
PORT=8001
```

### Database Connection Error
1. Ensure MySQL is running
2. Check credentials in `.env`
3. Create database if not exists: `CREATE DATABASE star_db;`

### Module Import Errors
Reinstall dependencies:
```bash
uv pip install -r requirements.txt --system --force-reinstall
```

## Testing

Run the test setup script:
```bash
python test_setup.py
```

This will verify all modules are properly installed and configured.
