#!/bin/bash

echo "Starting Star Reward System API with uv..."

# Check if uv is installed
if ! command -v uv &> /dev/null
then
    echo "uv is not installed. Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
fi

# Install dependencies using uv
echo "Installing dependencies..."
uv pip install -r requirements.txt

# Start the application with uvicorn through uv
echo "Starting FastAPI application..."
uv run python main.py
