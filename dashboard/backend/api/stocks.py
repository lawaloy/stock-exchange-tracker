"""
Stocks API endpoints
"""
from fastapi import APIRouter, HTTPException, Path, Query
from dashboard.backend.models.stock import StockDetail, CurrentData, ProjectionData, TechnicalData, HistoricalData, HistoricalPoint
from dashboard.backend.services.data_loader import get_data_loader
from datetime import datetime, timedelta

router = APIRouter()


@router.get("/{symbol}", response_model=StockDetail)
async def get_stock_detail(symbol: str = Path(..., description="Stock symbol")):
    """Get detailed information for a specific stock"""
    try:
        loader = get_data_loader()
        date = loader.get_latest_date()
        
        if not date:
            raise HTTPException(status_code=404, detail="No data available")
        
        # Load daily data
        daily_df = loader.load_daily_data()
        stock_daily = daily_df[daily_df['symbol'] == symbol.upper()]
        
        if stock_daily.empty:
            raise HTTPException(status_code=404, detail=f"Stock {symbol} not found")
        
        stock_row = stock_daily.iloc[0]
        
        # Build current data
        current_data = CurrentData(
            price=float(stock_row['close']),
            change=float(stock_row['change']),
            changePercent=float(stock_row['change_percent']),
            volume=int(stock_row.get('volume', 0)),
            marketCap=float(stock_row.get('market_cap', 0)) if 'market_cap' in stock_row else None
        )
        
        # Try to load projection data
        projection_data = None
        technical_data = None
        
        try:
            proj_df = loader.load_projections()
            stock_proj = proj_df[proj_df['symbol'] == symbol.upper()]
            
            if not stock_proj.empty:
                proj_row = stock_proj.iloc[0]
                
                # Calculate target date
                proj_date = datetime.strptime(date, "%Y-%m-%d")
                target_date = (proj_date + timedelta(days=5)).strftime("%Y-%m-%d")
                
                projection_data = ProjectionData(
                    targetDate=target_date,
                    targetPrice=float(proj_row['target_mid']),
                    expectedChange=float(proj_row['expected_change_percent']),
                    confidence=int(proj_row['confidence']),
                    recommendation=proj_row['recommendation'],
                    risk=proj_row['risk_level'],
                    trend=proj_row['trend']
                )
                
                # Build technical data if available
                technical_data = TechnicalData(
                    momentum=float(proj_row.get('momentum_score', 0)) if 'momentum_score' in proj_row else None,
                    volatility=float(proj_row.get('volatility_score', 0)) if 'volatility_score' in proj_row else None,
                    rsi=None  # Not available in current data
                )
        
        except Exception:
            # No projection data available
            pass
        
        return StockDetail(
            symbol=symbol.upper(),
            name=stock_row.get('name', symbol.upper()),
            currentData=current_data,
            projection=projection_data,
            technical=technical_data
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/{symbol}/historical", response_model=HistoricalData)
async def get_stock_historical(
    symbol: str = Path(..., description="Stock symbol"),
    days: int = Query(30, ge=1, le=365, description="Number of days of history")
):
    """Get historical data for a specific stock"""
    try:
        loader = get_data_loader()
        historical_records = loader.load_historical_data(symbol.upper(), days)
        
        if not historical_records:
            raise HTTPException(status_code=404, detail=f"No historical data found for {symbol}")
        
        historical_points = []
        for record in historical_records:
            projection = record.get('projection')
            
            historical_points.append(HistoricalPoint(
                date=record['date'],
                close=float(record['close']),
                change=float(record['change_percent']),
                volume=int(record.get('volume', 0)),
                projection=projection
            ))
        
        return HistoricalData(
            symbol=symbol.upper(),
            data=historical_points
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
