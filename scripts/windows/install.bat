@echo off
echo Creating Python virtual environment (venv)...
python -m venv venv
if %errorlevel% neq 0 (
    echo Failed to create virtual environment. Make sure Python is installed and in your PATH.
    pause
    exit /b 1
)

echo Installing required packages from requirements.txt into venv...
.\venv\Scripts\python.exe -m pip install -r ..\..\requirements.txt
if %errorlevel% neq 0 (
    echo Failed to install packages. Check requirements.txt and your internet connection.
    pause
    exit /b 1
)

echo Installation complete!
echo You can now run configure.bat to set up your API keys and settings.
pause