#!/bin/bash

# Script to start OPC UA vibration server in a screen session
# Location: /home/admin/SlowControls2x2/VibMon/opcua_server/start_opcua_in_screen.sh

SCRIPT_DIR="/home/admin/SlowControls2x2/VibMon/opcua_server"
SESSION_NAME="opcua"
PYTHON_SCRIPT="start_opcua.py"
VENV_NAME="opcua_env"

echo "Starting OPC UA Vibration Server in screen session..."

# Change to script directory
cd "$SCRIPT_DIR"

# Check if screen session already exists
if screen -list | grep -q "$SESSION_NAME"; then
    echo "Screen session '$SESSION_NAME' already exists!"
    echo "Use 'screen -r $SESSION_NAME' to attach to it"
    echo "Or kill it first with: screen -S $SESSION_NAME -X quit"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "$VENV_NAME" ]; then
    echo "Error: Virtual environment '$VENV_NAME' not found in $SCRIPT_DIR"
    exit 1
fi

# Check if Python script exists
if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo "Error: Python script '$PYTHON_SCRIPT' not found in $SCRIPT_DIR"
    exit 1
fi

# Start screen session with OPC UA server
screen -S "$SESSION_NAME" -dm bash -c "
    cd '$SCRIPT_DIR'
    source $VENV_NAME/bin/activate
    echo 'Virtual environment activated'
    echo 'Starting OPC UA server...'
    python $PYTHON_SCRIPT
"

# Check if screen session was created successfully
sleep 1
if screen -list | grep -q "$SESSION_NAME"; then
    echo "✓ OPC UA server started successfully in screen session '$SESSION_NAME'"
    echo ""
    echo "Useful commands:"
    echo "  View server output:    screen -r $SESSION_NAME"
    echo "  Detach from screen:    Ctrl+A, then D"
    echo "  Stop server:           screen -S $SESSION_NAME -X quit"
    echo "  List screen sessions:  screen -ls"
else
    echo "✗ Failed to start screen session"
    exit 1
fi
