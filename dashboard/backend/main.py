"""
FastAPI Backend for Stock Exchange Tracker Dashboard
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import sys

# Add parent directory to path to import from src
sys.path.append(str(Path(__file__).parent.parent.parent))

from dashboard.backend.api import market, projections, stocks, refresh

app = FastAPI(
    title="Stock Exchange Tracker API",
    description="API for stock market data, projections, and recommendations",
    version="0.3.0"
)

# CORS configuration for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(market.router, prefix="/api/market", tags=["Market"])
app.include_router(projections.router, prefix="/api/projections", tags=["Projections"])
app.include_router(stocks.router, prefix="/api/stocks", tags=["Stocks"])
app.include_router(refresh.router, prefix="/api", tags=["Refresh"])


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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
