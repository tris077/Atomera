@echo off
REM Build and push Atomera Boltz-2 Docker image to GitHub Container Registry
REM Usage: build_and_push_docker.bat

echo ============================================================
echo   Atomera Docker Build and Push Script (Windows)
echo ============================================================
echo.

REM Configuration
set GITHUB_USERNAME=tris077
set IMAGE_TAG=latest
set IMAGE_NAME=ghcr.io/%GITHUB_USERNAME%/atomera-boltz2:%IMAGE_TAG%

echo Image: %IMAGE_NAME%
echo.
echo This will:
echo   1. Build the Docker image (10-30 minutes due to model download)
echo   2. Push the image to GitHub Container Registry
echo.
set /p CONFIRM=Continue? (y/n):

if /i not "%CONFIRM%"=="y" (
    echo Cancelled.
    exit /b 0
)

echo.
echo [Step 1/2] Building Docker image...
echo This may take 10-30 minutes due to Boltz-2 model download
echo ============================================================
docker build -t %IMAGE_NAME% .

if errorlevel 1 (
    echo.
    echo ERROR: Docker build failed
    exit /b 1
)

echo.
echo [Step 2/2] Pushing image to GitHub Container Registry...
echo ============================================================
echo If you haven't logged in yet, you'll need to login first:
echo   docker login ghcr.io
echo   Username: %GITHUB_USERNAME%
echo   Password: Your GitHub Personal Access Token
echo.

docker push %IMAGE_NAME%

if errorlevel 1 (
    echo.
    echo ERROR: Docker push failed
    echo.
    echo You may need to login first:
    echo   docker login ghcr.io
    echo   Username: %GITHUB_USERNAME%
    echo   Password: Your GitHub Personal Access Token
    exit /b 1
)

echo.
echo ============================================================
echo   SUCCESS! Image pushed to registry
echo ============================================================
echo.
echo Your image is available at:
echo   %IMAGE_NAME%
echo.
echo Next steps:
echo   1. Go to RunPod console: https://www.runpod.io/console/serverless
echo   2. Find endpoint: lm0cjtlazfyx6f
echo   3. Stop all workers
echo   4. Start a new worker (will pull new image)
echo   5. Test with: cd backend ^&^& python test_job_submission.py
echo.
echo Build completed successfully!
pause
