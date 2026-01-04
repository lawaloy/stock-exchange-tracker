"""
Stock Exchange Tracker - Main Entry Point

This is a convenience wrapper that calls the main stock_tracker CLI module.
The actual implementation is in src/cli/stock_tracker.py
"""

import sys
from pathlib import Path

# Add parent directory to path to enable absolute imports
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.cli.stock_tracker import main

if __name__ == "__main__":
    main()
