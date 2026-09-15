@echo off
echo ===================================================
echo Starting AI/ML SVG Logo Generator Web Application
echo ===================================================

echo [1/2] Launching FastAPI Backend on http://127.0.0.1:8000...
start "SVG Logo Generator - Backend" cmd /k "cd backend && ..\.venv\Scripts\python.exe -m uvicorn app:app --port 8000 --reload"

timeout /t 2 /nobreak >nul

echo [2/2] Launching React Vite Frontend on http://localhost:5173...
start "SVG Logo Generator - Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo Both servers started!
echo Open your browser at: http://localhost:5173
echo ===================================================
pause
