@echo off
echo Starting Atomera servers...
echo.

echo Starting backend on port 8000...
cd backend
start "Atomera Backend" cmd /k "python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload"
cd ..

timeout /t 2 /nobreak >nul

echo Starting frontend on port 8080...
cd frontend
start "Atomera Frontend" cmd /k "npm run dev"
cd ..

timeout /t 3 /nobreak >nul

echo.
echo Servers should be starting...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:8080
echo.
echo Press any key to exit this window (servers will continue running)
pause >nul

