#!/bin/bash
# Script to set up daily automatic stock data updates (Unix/Mac)

echo "===================================="
echo "Stock Tracker - Scheduled Updates Setup"
echo "===================================="
echo ""

# Get the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PYTHON_SCRIPT="$SCRIPT_DIR/main.py"
PYTHON_CMD=$(which python3 || which python)

echo "Project Directory: $SCRIPT_DIR"
echo "Python Script: $PYTHON_SCRIPT"
echo "Python Command: $PYTHON_CMD"
echo ""

# Check if Python script exists
if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo "❌ ERROR: main.py not found at $PYTHON_SCRIPT"
    echo "Please run this script from the project root directory."
    exit 1
fi

# Detect OS
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS - use launchd
    echo "Detected macOS - Setting up launchd service..."
    echo ""
    
    PLIST_FILE="$HOME/Library/LaunchAgents/com.stocktracker.daily.plist"
    
    cat > "$PLIST_FILE" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.stocktracker.daily</string>
    <key>ProgramArguments</key>
    <array>
        <string>$PYTHON_CMD</string>
        <string>$PYTHON_SCRIPT</string>
    </array>
    <key>WorkingDirectory</key>
    <string>$SCRIPT_DIR</string>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>16</integer>
        <key>Minute</key>
        <integer>30</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>$SCRIPT_DIR/logs/scheduled_run.log</string>
    <key>StandardErrorPath</key>
    <string>$SCRIPT_DIR/logs/scheduled_run_error.log</string>
</dict>
</plist>
EOF

    # Load the plist
    launchctl load "$PLIST_FILE"
    
    echo "✅ SUCCESS! Scheduled task created successfully."
    echo ""
    echo "Service: com.stocktracker.daily"
    echo "Schedule: Daily at 4:30 PM"
    echo "Logs: $SCRIPT_DIR/logs/"
    echo ""
    echo "To uninstall:"
    echo "  launchctl unload $PLIST_FILE"
    echo "  rm $PLIST_FILE"
    
else
    # Linux - use cron
    echo "Detected Linux - Setting up cron job..."
    echo ""
    
    CRON_CMD="30 16 * * * cd $SCRIPT_DIR && $PYTHON_CMD $PYTHON_SCRIPT >> $SCRIPT_DIR/logs/scheduled_run.log 2>&1"
    
    # Check if cron job already exists
    if crontab -l 2>/dev/null | grep -q "$PYTHON_SCRIPT"; then
        echo "Cron job already exists. Removing old entry..."
        crontab -l 2>/dev/null | grep -v "$PYTHON_SCRIPT" | crontab -
    fi
    
    # Add new cron job
    (crontab -l 2>/dev/null; echo "$CRON_CMD") | crontab -
    
    echo "✅ SUCCESS! Cron job created successfully."
    echo ""
    echo "Schedule: Daily at 4:30 PM"
    echo "Logs: $SCRIPT_DIR/logs/scheduled_run.log"
    echo ""
    echo "To view cron jobs:"
    echo "  crontab -l"
    echo ""
    echo "To remove:"
    echo "  crontab -e"
    echo "  (then delete the line containing $PYTHON_SCRIPT)"
fi

echo ""
echo "The stock tracker will now run automatically every day!"
echo "Your dashboard will always show fresh data."
echo ""
