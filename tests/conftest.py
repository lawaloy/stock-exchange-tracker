"""Pytest configuration - add project root to path for imports."""

import sys
from pathlib import Path

# Add project root so "from src.xxx" and "from dashboard.xxx" work
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
