"""
Market API endpoints
"""
from fastapi import APIRouter, HTTPException, Query
from dashboard.backend.models.market import MarketOverview, MoversResponse, StockMover, IndexData
from dashboard.backend.services.data_loader import get_data_loader

router = APIRouter()


@router.get("/overview", response_model=MarketOverview)
async def get_market_overview():
    """Get market overview with statistics"""
    try:
        loader = get_data_loader()
        date = loader.get_latest_date()
        
        if not date:
            raise HTTPException(status_code=404, detail="No data available")
        
        # Load daily data
        df = loader.load_daily_data()
        
        # Calculate overall statistics
        total_stocks = len(df)
        gainers = len(df[df['change_percent'] > 0])
        losers = len(df[df['change_percent'] < 0])
        unchanged = len(df[df['change_percent'] == 0])
        
        avg_change = float(df['change_percent'].mean())
        max_change = float(df['change_percent'].max())
        min_change = float(df['change_percent'].min())
        
        # Calculate per-index statistics
        indices = {}
        if 'index_name' in df.columns:
            for index_name in df['index_name'].unique():
                index_df = df[df['index_name'] == index_name]
                indices[index_name.replace(' ', '')] = IndexData(
                    stocks=len(index_df),
                    avgChange=float(index_df['change_percent'].mean()),
                    gainers=len(index_df[index_df['change_percent'] > 0]),
                    losers=len(index_df[index_df['change_percent'] < 0])
                )
        
        return MarketOverview(
            date=date,
            totalStocks=total_stocks,
            gainers=gainers,
            losers=losers,
            unchanged=unchanged,
            averageChange=round(avg_change, 2),
            maxChange=round(max_change, 2),
            minChange=round(min_change, 2),
            indices=indices
        )
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/movers", response_model=MoversResponse)
async def get_top_movers(
    type: str = Query("gainers", pattern="^(gainers|losers)$"),
    limit: int = Query(10, ge=1, le=50)
):
    """Get top gainers or losers"""
    try:
        loader = get_data_loader()
        df = loader.load_daily_data()
        
        # Sort by change percentage
        if type == "gainers":
            sorted_df = df.nlargest(limit, 'change_percent')
        else:
            sorted_df = df.nsmallest(limit, 'change_percent')
        
        movers = []
        for _, row in sorted_df.iterrows():
            movers.append(StockMover(
                symbol=row['symbol'],
                name=row.get('name', row['symbol']),
                price=float(row['close']),
                change=float(row['change']),
                changePercent=float(row['change_percent']),
                volume=int(row.get('volume', 0))
            ))
        
        return MoversResponse(type=type, data=movers)
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
