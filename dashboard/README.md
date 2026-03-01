# Stock Exchange Tracker Dashboard

Modern, interactive web dashboard for visualizing stock market data, projections, and recommendations.

## Quick Start

### Prerequisites

- Python 3.12+
- Node.js 18+
- npm or yarn

### 1. Start the Backend

```bash
cd dashboard/backend

# Create virtual environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate
# Or Mac/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the server
python main.py
```

Backend will run on `http://localhost:8000`

### 2. Start the Frontend

```bash
cd dashboard/frontend

# Install dependencies
npm install

# Start the dev server
npm run dev
```

Frontend will run on `http://localhost:3000`

### 3. Open the Dashboard

Navigate to `http://localhost:3000` in your browser.

## Features

### Phase 1 MVP (Implemented)

✅ **Dashboard Overview**

- Market overview with KPI cards
- Top gainers/losers chart
- Recommendation distribution pie chart
- STRONG BUY opportunities section
- Filterable/sortable stock table
- Stock detail modal

✅ **API Endpoints**

- `/api/market/overview` - Market statistics
- `/api/market/movers` - Top gainers/losers
- `/api/summary` - Market summary (Expert or Learner)
- `/api/projections/summary` - Projections overview
- `/api/projections/opportunities` - Buy/Sell opportunities
- `/api/stocks/{symbol}` - Stock details
- `/api/stocks/{symbol}/historical` - Historical data

✅ **Technologies**

- FastAPI backend with pandas data loading
- React 18 + TypeScript frontend
- TailwindCSS for styling
- Recharts for visualizations
- Headless UI for modals

## Project Structure

```text
dashboard/
├── backend/              # FastAPI Backend
│   ├── main.py          # Entry point
│   ├── api/             # API endpoints
│   ├── models/          # Pydantic models
│   └── services/        # Data loading services
│
└── frontend/            # React Frontend
    ├── src/
    │   ├── components/  # React components
    │   ├── pages/       # Page components
    │   ├── services/    # API client
    │   ├── types/       # TypeScript types
    │   └── utils/       # Utilities
    └── package.json
```

## API Documentation

With the backend running, visit:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Development

### Backend Development

```bash
cd dashboard/backend
uvicorn main:app --reload --port 8000
```

### Frontend Development

```bash
cd dashboard/frontend
npm run dev
```

### Build for Production

**Backend:**

```bash
cd dashboard/backend
# Use the Dockerfile in the root or deploy to Railway/Render/Fly.io
```

**Frontend:**

```bash
cd dashboard/frontend
npm run build
# Deploy to Vercel/Netlify
```

## Environment Variables

**Backend:**

- `DATA_DIR` - Path to data directory (defaults to `../../data`)
- `CORS_ORIGINS` - Allowed CORS origins (defaults to localhost:3000)

**Frontend:**

- `VITE_API_URL` - Backend API URL (defaults to `http://localhost:8000`)

## Troubleshooting

### Backend Issues

#### "No data files found"

- Make sure you've run the stock tracker at least once to generate data files
- Check that the `data/` directory exists in the project root

#### CORS errors

- Backend allows localhost:3000 by default
- For production, update CORS settings in `backend/main.py`

### Frontend Issues

#### "Failed to fetch"

- Make sure the backend is running on port 8000
- Check browser console for specific errors

#### Components not styling correctly

- Run `npm install` to ensure all dependencies are installed
- TailwindCSS requires PostCSS - check that postcss.config.js exists

## What's Next?

**Next Priority:**

1. **Historical trends page** – Multi-day data, projection accuracy tracking, trend charts (partially implemented)
2. **Performance** – Code splitting, lazy loading
3. **Watchlist** – Save favorite stocks
4. **Keyboard shortcuts** – Quick navigation

See [DASHBOARD_DESIGN.md](../docs/DASHBOARD_DESIGN.md) for full Phase 2 design.

## Contributing

See [CONTRIBUTING.md](../../CONTRIBUTING.md) for guidelines.

## License

MIT License - See [LICENSE](../../LICENSE)
