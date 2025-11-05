@echo off
echo Starting Star Reward System API with uv...

:: Check if uv is installed
where uv >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo uv is not installed. Installing uv...
    powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
)

:: Install dependencies using uv
echo Installing dependencies...
uv pip install -r requirements.txt

:: Start the application with uvicorn through uv
echo Starting FastAPI application...
uv run python main.py
