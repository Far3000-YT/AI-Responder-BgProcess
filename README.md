# AI Responder using Gemini API

This project provides a background tool that uses the Google Gemini API to respond to questions based on screen content (via screenshot) or clipboard text. It runs silently and uses keyboard shortcuts. A small visual indicator shows when the AI is busy.

## Project Structure

Make sure you have the following structure, especially the `scripts` directory and its contents:

`AI-Responder-BgProcess/`
`├── .env`
`├── .gitignore`
`├── config.yaml`
`├── indicator.py`
`├── README.md`
`├── requirements.txt`
`├── run.py`
`├── .git/`
`├── main/`
`│   ├── a_config.py`
`│   ├── capture.py`
`│   ├── c_config.py`
`│   ├── env.py`
`│   └── status.py`
`├── __pycache__/`
`└── scripts/`
`    ├── windows/`
`    │   ├── install.bat`
`    │   ├── configure.bat`
`    │   └── run.bat`
`    └── linux-macos/`
`        ├── install.sh`
`        ├── configure.sh`
`        └── run.sh`

## Prerequisites

*   **Git:** To clone the repository.
*   **Python:** Version 3.7 or higher recommended. Make sure it's added to your system's PATH.

## Easy Setup with Scripts

This project includes scripts to simplify installation and running on Windows and Linux/macOS.

**1. Clone the Repository**

Open your terminal or command prompt and run:

`git clone <repository_url> # Replace <repository_url> with the actual URL`
`cd AI-Responder-BgProcess`

**2. Install Dependencies**

This step creates an isolated environment for the project's Python packages.

*   **Windows:** Navigate to the `scripts/windows` directory in your file explorer and double-click `install.bat`. Alternatively, open Command Prompt, `cd` into `scripts/windows`, and run `install.bat`. The script (`scripts/windows/install.bat`) contains:

    `@echo off`
    `echo Creating Python virtual environment (venv)...`
    `python -m venv venv`
    `if %errorlevel% neq 0 (`
    `    echo Failed to create virtual environment. Make sure Python is installed and in your PATH.`
    `    pause`
    `    exit /b 1`
    `)`
    ``
    `echo Installing required packages from requirements.txt into venv...`
    `.\venv\Scripts\python.exe -m pip install -r ..\..\requirements.txt`
    `if %errorlevel% neq 0 (`
    `    echo Failed to install packages. Check requirements.txt and your internet connection.`
    `    pause`
    `    exit /b 1`
    `)`
    ``
    `echo Installation complete!`
    `echo You can now run configure.bat to set up your API keys and settings.`
    `pause`

*   **Linux/macOS:** Open your terminal, navigate to the `scripts/linux-macos` directory (`cd scripts/linux-macos`), make the script executable (`chmod +x install.sh`), and run it (`./install.sh`). The script (`scripts/linux-macos/install.sh`) contains:

    `#!/bin/bash`
    ``
    `echo "Creating Python virtual environment (venv)..."`
    `python3 -m venv venv`
    `if [ $? -ne 0 ]; then`
    `    echo "Failed to create virtual environment. Make sure Python 3 is installed."`
    `    exit 1`
    `fi`
    ``
    `echo "Installing required packages from requirements.txt into venv..."`
    `venv/bin/pip install -r ../../requirements.txt`
    `if [ $? -ne 0 ]; then`
    `    echo "Failed to install packages. Check requirements.txt and your internet connection."`
    `    exit 1`
    `fi`
    ``
    `echo "Installation complete!"`
    `echo "You can now run ./configure.sh to set up your API keys and settings."`

Wait for the installation to complete.

**3. Configure API Keys and Settings**

You need to tell the script your Google Gemini API key(s) and adjust settings.

*   **Get API Key(s):** Obtain one or two API keys from [Google AI Studio](https://aistudio.google.com/app/apikey). You only need a second key if you plan to enable `double_requests` in the config.
*   **Run Configure Script:**
    *   **Windows:** Double-click `configure.bat` in the `scripts/windows` directory. Script content (`scripts/windows/configure.bat`):

        `@echo off`
        `echo Opening .env file (for API Keys)...`
        `start "" ..\..\.env`
        `timeout /t 1 /nobreak > nul`
        ``
        `echo Opening config.yaml file (for settings)...`
        `start "" ..\..\config.yaml`
        ``
        `echo Please edit these files and save them.`
        `echo Press any key when you are done...`
        `pause`

    *   **Linux/macOS:** In the terminal, from the `scripts/linux-macos` directory, make the script executable (`chmod +x configure.sh`) and run it (`./configure.sh`). Script content (`scripts/linux-macos/configure.sh`):

        `#!/bin/bash`
        ``
        `echo "Attempting to open .env and config.yaml in your default editor..."`
        ``
        `# Try xdg-open (common on Linux) or open (macOS)`
        `if command -v xdg-open &> /dev/null; then`
        `    xdg-open ../../.env`
        `    xdg-open ../../config.yaml`
        `elif command -v open &> /dev/null; then`
        `    open ../../.env`
        `    open ../../config.yaml`
        `else`
        `    echo "Could not find xdg-open or open."`
        `    echo "Please open .env and config.yaml in your text editor manually."`
        `fi`
        ``
        `echo "Please edit these files and save them."`
        `read -p "Press Enter when you are done..."`

*   **Edit Files:** The script will attempt to open two files:
    *   `.env`: Add your primary API key like this: `GEMINI_KEY=YOUR_API_KEY_HERE`. If using `double_requests`, also add `API_KEY_GEMINI2=YOUR_SECOND_KEY_HERE`.
    *   `config.yaml`: Review and change settings like `model_name`, `base_prompt`, and keyboard shortcuts (`screenshot_cmd`, `point_select`, `ctrl_c`). **Do not change the variable names, only their values.** Make sure the `base_prompt` asks for the output format you want.
*   **Save** both files after editing. Press Enter/any key in the configuration script window when done.

**4. Run the Application**

This script starts both the main AI responder and the status indicator.

*   **Windows:** Double-click `run.bat` in the `scripts/windows` directory. Two new command prompt windows will open, one for the main script and one for the indicator. Keep these windows open while you use the tool. Script content (`scripts/windows/run.bat`):

    `@echo off`
    `echo Starting AI Responder (run.py)...`
    `start "AI Responder" cmd /c ".\venv\Scripts\activate.bat && python ..\..\run.py"`
    ``
    `timeout /t 1 /nobreak > nul`
    ``
    `echo Starting Status Indicator (indicator.py)...`
    `start "Status Indicator" cmd /c ".\venv\Scripts\activate.bat && python ..\..\indicator.py"`
    ``
    `echo Both scripts started in separate windows.`
    `echo To stop them, close their respective command prompt windows.`

*   **Linux/macOS:** In the terminal, from the `scripts/linux-macos` directory, make the script executable (`chmod +x run.sh`) and run it (`./run.sh`). The scripts will start in the background. The terminal will show you the Process IDs (PIDs) needed to stop them later and the log files (`run.log`, `indicator.log`). Script content (`scripts/linux-macos/run.sh`):

    `#!/bin/bash`
    ``
    `# Activate virtual environment`
    `source venv/bin/activate`
    `if [ $? -ne 0 ]; then`
    `    echo "Failed to activate virtual environment."`
    `    exit 1`
    `fi`
    ``
    `echo "Starting AI Responder (run.py) in the background..."`
    `nohup python3 ../../run.py > run.log 2>&1 &`
    `RUN_PID=$!`
    `echo "AI Responder started with PID $RUN_PID. Output logged to run.log."`
    ``
    `sleep 1 # Give it a second to start`
    ``
    `echo "Starting Status Indicator (indicator.py) in the background..."`
    `nohup python3 ../../indicator.py > indicator.log 2>&1 &`
    `INDICATOR_PID=$!`
    `echo "Status Indicator started with PID $INDICATOR_PID. Output logged to indicator.log."`
    ``
    `echo ""`
    `echo "Both scripts are running in the background."`
    `echo "To stop them, use the kill command:"`
    `echo "kill $RUN_PID"`
    `echo "kill $INDICATOR_PID"`
    `echo ""`
    `echo "You can view their logs with:"`
    `echo "tail -f run.log"`
    `echo "tail -f indicator.log"`
    ``
    `# Deactivate venv (optional, script ends anyway)`
    `# deactivate`

## Usage

Once the application is running (via `run.bat` or `run.sh`):

1.  **Screenshot:** Press the `screenshot_cmd` hotkey defined in `config.yaml`. Then press the `point_select` key twice to define the top-left and bottom-right corners of the area you want to capture.
2.  **Clipboard Text:** If `ctrl_c` is enabled in `config.yaml`, simply copy some text to your clipboard (using Ctrl+C) and the script *should* detect it and process it. (Note: Using Ctrl+C as a trigger can sometimes be unreliable; a unique hotkey might be better if you encounter issues).
3.  **Wait:** The small indicator square (usually top-left of your screen) will turn yellow while processing.
4.  **Result:** The AI's response will be automatically copied to your clipboard. Paste it (Ctrl+V) wherever you need it.
5.  **Cooldown:** There's a short cooldown between requests (configurable in `config.yaml`) to prevent accidental spamming.

## Stopping the Application

*   **Windows:** Simply close the two command prompt windows that were opened by `run.bat`.
*   **Linux/macOS:** Use the `kill` command with the PIDs shown when you ran `./run.sh`. For example: `kill <PID_of_run.py>` and `kill <PID_of_indicator.py>`.

## Troubleshooting

*   **Script Errors:** Ensure Python and Git are installed correctly and accessible from your terminal/command prompt.
*   **API Key Errors:** Double-check `.env` for typos and make sure the keys are valid. If `double_requests` is `True`, ensure `API_KEY_GEMINI2` is also set.
*   **Hotkey Issues:** Verify the hotkey strings in `config.yaml` work with your OS and keyboard layout. The `keyboard` library can sometimes be tricky. Try simpler combos (like `alt+s`) if default ones fail.
*   **No Response/Indicator Stuck:** Check the command prompt windows (Windows) or the `.log` files (Linux/macOS) for error messages.