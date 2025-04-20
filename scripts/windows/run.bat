@echo off
echo Starting AI Responder (run.py)...
start "AI Responder" cmd /c ".\venv\Scripts\activate.bat && python ..\..\run.py"

timeout /t 1 /nobreak > nul

echo Starting Status Indicator (indicator.py)...
start "Status Indicator" cmd /c ".\venv\Scripts\activate.bat && python ..\..\indicator.py"

echo Both scripts started in separate windows.
echo To stop them, close their respective command prompt windows.