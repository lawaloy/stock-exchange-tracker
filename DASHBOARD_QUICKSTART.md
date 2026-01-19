# Dashboard Quick Start Guide

## 🎉 Your Dashboard is Ready

The Stock Exchange Tracker now has a fully functional web dashboard built with FastAPI and React.

## Starting the Dashboard

### Option 1: Using Startup Scripts (Easiest)

**Windows:**

```bash
cd dashboard
start-dashboard.bat
```

**Mac/Linux:**

```bash
cd dashboard
chmod +x start-dashboard.sh
./start-dashboard.sh
```

### Option 2: Manual Start

**Terminal 1 - Backend:**

```bash
cd dashboard/backend
python main.py
```

**Terminal 2 - Frontend:**

```bash
cd dashboard/frontend
npm install  # First time only
npm run dev
```

## Accessing the Dashboard

Once both servers are running:

- **Frontend Dashboard**: <http://localhost:3000>
- **Backend API**: <http://localhost:8000>
- **API Documentation**: <http://localhost:8000/docs>

## What You'll See

### Dashboard Overview

1. **KPI Cards** (Top of page)
   - Stocks Tracked (196 stocks)
   - Average Confidence (70.7%)
   - Expected Market Move (+0.23%)
   - Strong Buy Opportunities (11)

2. **Top Movers Chart** (Left)
   - Bar chart showing top 5 gainers and losers
   - Color-coded green (gainers) and red (losers)

3. **Recommendation Distribution** (Right)
   - Pie chart showing STRONG BUY, BUY, HOLD, SELL, STRONG SELL
   - Interactive with percentages

4. **STRONG BUY Opportunities**
   - Top 5 best trading opportunities
   - Shows current price → target price
   - Confidence scores and risk levels
   - Click any card to see details

5. **All Stocks Table**
   - Complete list of all 177 projections
   - Search by symbol or name
   - Filter by recommendation type
   - Sort by any column
   - Click any row to see stock details

### 🔍 Stock Detail Modal

Click any stock to see:

- Current price and change
- 5-day price projection
- Target price and expected change
- Recommendation (STRONG BUY to STRONG SELL)
- Confidence score with visual progress bar
- Risk level (Low/Medium/High)
- Trend (Bullish/Bearish/Neutral)
- Key metrics (volume, momentum, volatility)

## Features You Can Use

✅ **Search**: Type any stock symbol or company name  
✅ **Filter**: Filter by BUY, HOLD, or SELL recommendations  
✅ **Sort**: Click table headers to sort  
✅ **Paginate**: Navigate through 20 stocks per page  
✅ **Details**: Click any stock for detailed analysis  

## Troubleshooting

### Backend Won't Start

#### Error: "No data files found"

- Run the stock tracker first: `python main.py` (from project root)
- This generates the data files the dashboard needs

#### Error: "Port 8000 already in use"

- Stop any other processes using port 8000
- Or change the port in `dashboard/backend/main.py`

### Frontend Won't Start

#### Error: "npm command not found"

- Install Node.js from <https://nodejs.org> (version 18+)

#### Error: "Failed to fetch"

- Make sure the backend is running on port 8000
- Check for CORS errors in browser console

#### Dependencies not installing

```bash
cd dashboard/frontend
rm -rf node_modules package-lock.json
npm install
```

## API Endpoints (for developers)

All endpoints are documented at <http://localhost:8000/docs>

**Market Endpoints:**

- `GET /api/market/overview` - Market statistics
- `GET /api/market/movers?type=gainers&limit=10` - Top movers

**Projections Endpoints:**

- `GET /api/projections/summary` - Projections summary
- `GET /api/projections/opportunities?type=STRONG_BUY&limit=10` - Opportunities

**Stock Endpoints:**

- `GET /api/stocks/{symbol}` - Stock details
- `GET /api/stocks/{symbol}/historical?days=30` - Historical data

## Next Steps

1. **Explore the Dashboard**: Click around and explore all features
2. **Check Different Stocks**: Search for your favorite stocks
3. **Review Opportunities**: Look at STRONG BUY recommendations
4. **Read the Docs**: See `dashboard/README.md` for more details
5. **Deploy to Production**: See deployment guides in the design doc

## What's Coming Next?

See [CHANGELOG.md](CHANGELOG.md) for planned features:

- Historical trends with time-series charts
- Dark mode
- Real-time updates via WebSocket
- User authentication and watchlists
- Enhanced mobile experience

## Need Help?

- **Dashboard Docs**: See `dashboard/README.md`
- **Design Specs**: See `docs/DASHBOARD_DESIGN.md`
- **Main Docs**: See main `README.md`
- **Issues**: Open an issue on GitHub

---
