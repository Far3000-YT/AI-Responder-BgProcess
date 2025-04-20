#!/bin/bash

echo "Attempting to open .env and config.yaml in your default editor..."

# Try xdg-open (common on Linux) or open (macOS)
if command -v xdg-open &> /dev/null; then
    xdg-open ../../.env
    xdg-open ../../config.yaml
elif command -v open &> /dev/null; then
    open ../../.env
    open ../../config.yaml
else
    echo "Could not find xdg-open or open."
    echo "Please open .env and config.yaml in your text editor manually."
fi

echo "Please edit these files and save them."
read -p "Press Enter when you are done..."