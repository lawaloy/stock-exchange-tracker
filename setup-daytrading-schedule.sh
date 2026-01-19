#!/bin/bash
# Day Trading Schedule Setup - 4 Updates During Market Hours (Mon-Fri only)

echo "===================================="
echo "Stock Tracker - Day Trading Schedule"
echo "===================================="
echo ""

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PYTHON_SCRIPT="$SCRIPT_DIR/main.py"
PYTHON_CMD=$(which python3 || which python)

echo "Project Directory: $SCRIPT_DIR"
echo "Python Script: $PYTHON_SCRIPT"
echo "Python Command: $PYTHON_CMD"
echo ""

# Check if Python script exists
if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo "❌ ERROR: main.py not found"
    exit 1
fi

# Detect OS
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS - use launchd
    echo "Detected macOS - Setting up 4 launchd services..."
    echo ""
    
    TIMES=("09:00" "12:00" "15:00")
    LABELS=("0900" "1200" "1500")
    NAMES=("Market Open" "Midday" "Pre-Close")
    
    for i in {0..2}; do
        HOUR="${TIMES[$i]%%:*}"
        MINUTE="${TIMES[$i]##*:}"
        LABEL="com.stocktracker.daytrading.${LABELS[$i]}"
        PLIST_FILE="$HOME/Library/LaunchAgents/$LABEL.plist"
        
        echo "[$(($i+1))/4] Creating ${NAMES[$i]} task (${TIMES[$i]})..."
        
        cat > "$PLIST_FILE" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>$LABEL</string>
    <key>ProgramArguments</key>
    <array>
        <string>$PYTHON_CMD</string>
        <string>$PYTHON_SCRIPT</string>
        <string>--top-n</string>
        <string>50</string>
    </array>
    <key>WorkingDirectory</key>
    <string>$SCRIPT_DIR</string>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Weekday</key>
        <integer>1</integer>
        <key>Hour</key>
        <integer>$HOUR</integer>
        <key>Minute</key>
        <integer>$MINUTE</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>$SCRIPT_DIR/logs/daytrading_${LABELS[$i]}.log</string>
    <key>StandardErrorPath</key>
    <string>$SCRIPT_DIR/logs/daytrading_${LABELS[$i]}_error.log</string>
</dict>
</plist>
EOF
        
        launchctl load "$PLIST_FILE"
    done
    
    echo ""
    echo "✅ SUCCESS! All 3 scheduled tasks created!"
    
else
    # Linux - use cron
    echo "Detected Linux - Setting up cron jobs..."
    echo ""
    
    # Remove old entries
    crontab -l 2>/dev/null | grep -v "$PYTHON_SCRIPT --top-n 50" | crontab -
    
    # Add new cron jobs (Mon-Fri only)
    (crontab -l 2>/dev/null; cat << EOF
# Stock Tracker - Day Trading Schedule (Mon-Fri only)
0 9 * * 1-5 cd $SCRIPT_DIR && $PYTHON_CMD $PYTHON_SCRIPT --top-n 50 >> $SCRIPT_DIR/logs/daytrading_0900.log 2>&1
0 12 * * 1-5 cd $SCRIPT_DIR && $PYTHON_CMD $PYTHON_SCRIPT --top-n 50 >> $SCRIPT_DIR/logs/daytrading_1200.log 2>&1
0 15 * * 1-5 cd $SCRIPT_DIR && $PYTHON_CMD $PYTHON_SCRIPT --top-n 50 >> $SCRIPT_DIR/logs/daytrading_1500.log 2>&1
EOF
) | crontab -
    
    echo "✅ SUCCESS! All 3 cron jobs created!"
fi

echo ""
echo "Schedule Summary:"
echo "├── 9:00 AM  - Market Open (top 50 stocks)"
echo "├── 12:00 PM - Midday Update"
echo "└── 3:00 PM  - Pre-Close Update"
echo ""
echo "Days: Monday - Friday only (market days)"
echo "API Usage: 3 updates × 60 calls = 180 calls/day ✅"
echo ""
echo "Your dashboard will auto-update throughout the trading day!"
echo ""
