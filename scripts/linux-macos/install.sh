#!/bin/bash

echo "Creating Python virtual environment (venv)..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "Failed to create virtual environment. Make sure Python 3 is installed."
    exit 1
fi

echo "Installing required packages from requirements.txt into venv..."
venv/bin/pip install -r ../../requirements.txt
if [ $? -ne 0 ]; then
    echo "Failed to install packages. Check requirements.txt and your internet connection."
    exit 1
fi

echo "Installation complete!"
echo "You can now run ./configure.sh to set up your API keys and settings."