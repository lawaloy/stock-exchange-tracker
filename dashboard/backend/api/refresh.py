"""
Refresh API endpoints - Trigger stock tracker to fetch new data
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
import subprocess
import sys
from pathlib import Path
from datetime import datetime
import threading

router = APIRouter()

# Track refresh status
refresh_status = {
    "is_running": False,
    "last_refresh": None,
    "last_status": None,
    "progress": None
}


class RefreshResponse(BaseModel):
    status: str
    message: str
    last_refresh: str | None
    is_running: bool


class RefreshStatusResponse(BaseModel):
    is_running: bool
    last_refresh: str | None
    last_status: str | None
    progress: str | None


def run_stock_tracker():
    """Run the stock tracker in a separate process"""
    global refresh_status
    
    try:
        refresh_status["is_running"] = True
        refresh_status["progress"] = "Starting stock tracker..."
        
        # Get the project root (3 levels up from this file)
        project_root = Path(__file__).parent.parent.parent.parent
        main_script = project_root / "main.py"
        
        if not main_script.exists():
            refresh_status["last_status"] = "error"
            refresh_status["progress"] = f"Stock tracker not found at {main_script}"
            refresh_status["is_running"] = False
            return
        
        # Run the stock tracker
        refresh_status["progress"] = "Fetching latest data..."
        
        result = subprocess.run(
            [sys.executable, str(main_script)],
            cwd=str(project_root),
            capture_output=True,
            text=True,
            timeout=600  # 10 minute timeout
        )
        
        if result.returncode == 0:
            refresh_status["last_status"] = "success"
            refresh_status["last_refresh"] = datetime.now().isoformat()
            refresh_status["progress"] = "Data refresh completed successfully!"
        else:
            refresh_status["last_status"] = "error"
            refresh_status["progress"] = f"Error: {result.stderr[:200]}"
            
    except subprocess.TimeoutExpired:
        refresh_status["last_status"] = "timeout"
        refresh_status["progress"] = "Refresh timed out after 10 minutes"
    except Exception as e:
        refresh_status["last_status"] = "error"
        refresh_status["progress"] = f"Error: {str(e)}"
    finally:
        refresh_status["is_running"] = False


@router.post("/refresh", response_model=RefreshResponse)
async def trigger_refresh(background_tasks: BackgroundTasks):
    """
    Trigger the stock tracker to fetch fresh data
    
    This will:
    1. Run the stock tracker (main.py)
    2. Fetch latest data from Finnhub API
    3. Generate new projections
    4. Save updated CSV/JSON files
    5. Dashboard will automatically show new data
    """
    if refresh_status["is_running"]:
        return RefreshResponse(
            status="already_running",
            message="Data refresh is already in progress. Please wait.",
            last_refresh=refresh_status.get("last_refresh"),
            is_running=True
        )
    
    # Start refresh in background
    thread = threading.Thread(target=run_stock_tracker, daemon=True)
    thread.start()
    
    return RefreshResponse(
        status="started",
        message="Data refresh started. This will take 3-5 minutes.",
        last_refresh=refresh_status.get("last_refresh"),
        is_running=True
    )


@router.get("/refresh/status", response_model=RefreshStatusResponse)
async def get_refresh_status():
    """Get the current status of data refresh"""
    return RefreshStatusResponse(
        is_running=refresh_status["is_running"],
        last_refresh=refresh_status.get("last_refresh"),
        last_status=refresh_status.get("last_status"),
        progress=refresh_status.get("progress")
    )
