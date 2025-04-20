@echo off
echo Opening .env file (for API Keys)...
start "" ..\..\.env
timeout /t 1 /nobreak > nul

echo Opening config.yaml file (for settings)...
start "" ..\..\config.yaml

echo Please edit these files and save them.
echo Press any key when you are done...
pause