@echo off
echo 🧪 Running BoltzService Tests
echo ========================================

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.8+ and try again.
    pause
    exit /b 1
)

echo ✅ Python found
echo.

REM Install test dependencies if needed
echo 📦 Installing test dependencies...
pip install -r requirements-test.txt >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Some dependencies may not be installed. Continuing anyway...
)

echo.
echo 🚀 Running tests...
echo.

REM Run the integration tests first (they're simpler)
echo 📋 Running integration tests...
python test_integration.py
if errorlevel 1 (
    echo ❌ Integration tests failed
    echo.
    echo 💡 Try running individual tests:
    echo    python test_integration.py
    echo    python -m pytest test_boltz_service.py -v
    pause
    exit /b 1
)

echo.
echo 📋 Running unit tests...
python -m pytest test_boltz_service.py -v
if errorlevel 1 (
    echo ❌ Unit tests failed
    pause
    exit /b 1
)

echo.
echo 🎉 All tests passed!
echo.
echo 💡 Next steps:
echo    - Test with real Boltz-2 installation
echo    - Add more edge case tests
echo    - Run with coverage: pytest --cov=services.boltz_service --cov-report=html
echo.

pause
