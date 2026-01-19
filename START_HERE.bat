@echo off
echo.
echo ===============================================
echo    EVOLUTION OF TODO - STARTUP SCRIPT
echo ===============================================
echo.
echo This script will start the backend server.
echo.
echo Make sure you have:
echo 1. Python 3.11+ installed
echo 2. Node.js installed (for frontend)
echo 3. Dependencies installed (run 'pip install -r requirements.txt' in backend)
echo.
echo ===============================================
echo.
echo Starting backend server on http://localhost:8000
echo.
echo Press Ctrl+C to stop the server
echo.
cd backend
python -m uvicorn src.main:app --reload --port 8000
pause