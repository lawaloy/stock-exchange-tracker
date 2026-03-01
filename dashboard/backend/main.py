"""
FastAPI Backend for Stock Exchange Tracker Dashboard
"""
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import sys
import os

# Add parent directory to path to import from src
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

# Load .env from project root so FINNHUB_API_KEY is available for name enrichment
try:
    from dotenv import load_dotenv
    load_dotenv(project_root / ".env")
except ImportError:
    pass

from dashboard.backend.api import market, projections, stocks, refresh, history
from dashboard.backend.api.market import get_market_summary

app = FastAPI(
    title="Stock Exchange Tracker API",
    description="API for stock market data, projections, and recommendations",
    version="0.3.0"
)

# CORS configuration for local development
default_origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:3001",
    "http://localhost:3002",
    "http://localhost:3003",
    "http://localhost:3004",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
cors_env = os.getenv("CORS_ORIGINS", "")
env_origins = [origin.strip() for origin in cors_env.split(",") if origin.strip()]
origins = env_origins or default_origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(market.router, prefix="/api/market", tags=["Market"])
app.include_router(projections.router, prefix="/api/projections", tags=["Projections"])
app.include_router(stocks.router, prefix="/api/stocks", tags=["Stocks"])
app.include_router(refresh.router, prefix="/api", tags=["Refresh"])
app.include_router(history.router, prefix="/api/history", tags=["History"])


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Stock Exchange Tracker API",
        "version": "0.3.0"
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.get("/api/data-info")
async def data_info():
    """Data status: path, latest date, and whether we need to fetch for the most recent trading day."""
    from dashboard.backend.services.data_loader import get_data_loader, get_most_recent_trading_day
    loader = get_data_loader()
    target_trading_day = get_most_recent_trading_day()
    return {
        "data_dir": str(loader.data_dir),
        "latest_date": loader.get_latest_date(),
        "target_trading_day": target_trading_day,
        "needs_fetch": loader.needs_fetch_for_latest_trading_day(),
        "available_dates": loader.get_available_dates()[:5],
    }


@app.get("/api/summary")
async def api_summary():
    """Market summary (AI or demo)."""
    return await get_market_summary()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
