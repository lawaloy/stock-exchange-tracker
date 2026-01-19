"""
Refresh API endpoints - Trigger stock tracker to fetch new data
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
import subprocess
import sys
import os
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

_refresh_process: subprocess.Popen | None = None
_refresh_cancel_event = threading.Event()


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
    global _refresh_process
    try:
        refresh_status["is_running"] = True
        refresh_status["progress"] = "Starting stock tracker..."
        refresh_status["last_status"] = None
        _refresh_cancel_event.clear()
        
        # Get the project root (3 levels up from this file)
        project_root = Path(__file__).parent.parent.parent.parent
        main_script = project_root / "main.py"
        
        if not main_script.exists():
            refresh_status["last_status"] = "error"
            refresh_status["progress"] = f"Stock tracker not found at {main_script}"
            refresh_status["is_running"] = False
            return
        
        # Run the stock tracker (default to top 50 for day-trading mode)
        top_n_value = os.getenv("REFRESH_TOP_N", "50")
        try:
            top_n = max(0, int(top_n_value))
        except ValueError:
            top_n = 50

        command = [sys.executable, str(main_script)]
        if top_n:
            command.extend(["--top-n", str(top_n)])

        quote_only = os.getenv("REFRESH_QUOTE_ONLY", "1").lower() in {"1", "true", "yes"}
        if quote_only:
            command.append("--quote-only")

        no_screener = os.getenv("REFRESH_NO_SCREENER", "1").lower() in {"1", "true", "yes"}
        if no_screener:
            command.append("--no-screener")

        refresh_status["progress"] = "Fetching latest data..."

        _refresh_process = subprocess.Popen(
            command,
            cwd=str(project_root),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        try:
            stdout, stderr = _refresh_process.communicate(timeout=600)
        except subprocess.TimeoutExpired:
            _refresh_process.kill()
            stdout, stderr = _refresh_process.communicate()
            refresh_status["last_status"] = "timeout"
            refresh_status["progress"] = "Refresh timed out after 10 minutes"
            return

        if _refresh_cancel_event.is_set():
            refresh_status["last_status"] = "cancelled"
            refresh_status["progress"] = "Refresh cancelled."
            return

        if _refresh_process.returncode == 0:
            refresh_status["last_status"] = "success"
            refresh_status["last_refresh"] = datetime.now().isoformat()
            refresh_status["progress"] = "Data refresh completed successfully!"
        else:
            refresh_status["last_status"] = "error"
            error_output = (stderr or stdout or "").strip()
            if error_output:
                lines = [line.strip() for line in error_output.splitlines() if line.strip()]
                snippet = " | ".join(lines[-3:])[:300]
                refresh_status["progress"] = f"Error: {snippet}"
            else:
                refresh_status["progress"] = "Error: Refresh failed. Check backend logs."
    except Exception as e:
        refresh_status["last_status"] = "error"
        refresh_status["progress"] = f"Error: {str(e)}"
    finally:
        _refresh_process = None
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
        message="Background refresh started. Latest data will load when ready.",
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


@router.post("/refresh/cancel", response_model=RefreshStatusResponse)
async def cancel_refresh():
    """Cancel the current refresh job if running."""
    if not refresh_status["is_running"]:
        raise HTTPException(status_code=400, detail="No refresh in progress.")

    refresh_status["progress"] = "Cancelling refresh..."
    refresh_status["last_status"] = "cancelled"
    _refresh_cancel_event.set()

    if _refresh_process and _refresh_process.poll() is None:
        _refresh_process.terminate()
        try:
            _refresh_process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            _refresh_process.kill()

    refresh_status["is_running"] = False

    return RefreshStatusResponse(
        is_running=refresh_status["is_running"],
        last_refresh=refresh_status.get("last_refresh"),
        last_status=refresh_status.get("last_status"),
        progress=refresh_status.get("progress")
    )
