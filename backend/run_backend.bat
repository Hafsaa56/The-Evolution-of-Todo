@echo off
REM Run Todo Backend Server
cd /d "%~dp0"
echo Starting backend server on http://localhost:8000...

REM Set Python path for imports
set PYTHONPATH=%CD%

REM Activate virtual environment and run
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
)

REM Run uvicorn
uvicorn main:app --reload --host 0.0.0.0 --port 8000
