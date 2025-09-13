@echo off
echo 🧬 Atomera API Testing
echo ======================

echo.
echo Checking Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found in PATH
    echo.
    echo Please install Python 3.10+ from python.org
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo ✅ Python found
echo.

echo Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

echo ✅ Dependencies installed
echo.

echo 🚀 Starting server...
echo The server will start at http://localhost:8000
echo.
echo To test the API:
echo 1. Open http://localhost:8000/docs in your browser
echo 2. Or run: python test_simple.py
echo.
echo Press Ctrl+C to stop the server
echo ======================

python start.py

pause
