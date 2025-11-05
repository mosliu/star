# ============================================
# Stage 1: Build Frontend
# ============================================
FROM node:20-alpine AS frontend-builder

WORKDIR /build
COPY ./frontend .
RUN npm install
RUN npm run build

# ============================================
# Stage 2: Build Backend (Python FastAPI)
# ============================================
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Copy Python backend files
COPY ./python_backend/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY ./python_backend .

# Create necessary directories
RUN mkdir -p /app/logs /app/uploads

# Copy frontend build output
COPY --from=frontend-builder /build/dist /app/static

# Expose FastAPI port
EXPOSE 8000

# Start command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
