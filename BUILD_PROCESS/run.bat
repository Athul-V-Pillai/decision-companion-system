cd "C:\Users\Athul V   Pillai\OneDrive\Desktop\Decision Companion System\decision-companion"
run.batcd "C:\Users\Athul V   Pillai\OneDrive\Desktop\Decision Companion System\decision-companion"
run.batcd "C:\Users\Athul V   Pillai\OneDrive\Desktop\Decision Companion System\decision-companion"
run.bat@echo off
setlocal enabledelayedexpansion
REM Decision Companion System - Quick Start Script for Windows

cd /d "%~dp0"

echo.
echo ===================================
echo Decision Companion System Startup
echo ===================================
echo.

REM Activate virtual environment
if exist ".venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call .venv\Scripts\activate.bat
) else if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo Creating virtual environment...
    python -m venv .venv
    call .venv\Scripts\activate.bat
)

REM Install requirements
echo Installing dependencies...
pip install Flask==2.3.3 Werkzeug==2.3.7 --quiet

REM Run Flask app
echo.
echo ===================================
echo Starting Flask server...
echo ===================================
echo.
echo Open your browser and navigate to:
echo http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.

python app.py

pause
