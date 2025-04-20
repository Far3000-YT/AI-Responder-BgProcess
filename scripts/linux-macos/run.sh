#!/bin/bash

# Activate virtual environment
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "Failed to activate virtual environment."
    exit 1
fi

echo "Starting AI Responder (run.py) in the background..."
nohup python3 ../../run.py > run.log 2>&1 &
RUN_PID=$!
echo "AI Responder started with PID $RUN_PID. Output logged to run.log."

sleep 1 # Give it a second to start

echo "Starting Status Indicator (indicator.py) in the background..."
nohup python3 ../../indicator.py > indicator.log 2>&1 &
INDICATOR_PID=$!
echo "Status Indicator started with PID $INDICATOR_PID. Output logged to indicator.log."

echo ""
echo "Both scripts are running in the background."
echo "To stop them, use the kill command:"
echo "kill $RUN_PID"
echo "kill $INDICATOR_PID"
echo ""
echo "You can view their logs with:"
echo "tail -f run.log"
echo "tail -f indicator.log"

# Deactivate venv (optional, script ends anyway)
# deactivate