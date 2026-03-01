# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned for Future Releases

- Historical trends page with time-series analysis and projection accuracy tracking
- Full alert and notification system
- Real-time WebSocket updates
- User authentication and watchlists

## [0.3.1] - 2026-02-10

### Added

- **Dashboard Dark Mode**: Theme toggle with system preference detection and localStorage persistence
- **Dashboard Export**: CSV/PNG/PDF export for dashboard, stock table, and summary with clear labels per export target
- **Enhanced Mobile Layout**: Responsive design with horizontal scroll for stock tables

### Changed

- **Data Loader**: Uses date in filename (YYYY-MM-DD) instead of file mtime for latest data on startup and refresh
- **Header Layout**: Theme toggle moved to far right

## [0.3.0] - 2026-01-14

### Added

- **Web Dashboard**: Modern, interactive dashboard for visualizing stock data and projections
  - Real-time market overview with KPI cards (stocks tracked, confidence, expected move)
  - Interactive bar chart for top gainers/losers
  - Pie chart for recommendation distribution
  - Filterable and sortable stock table with pagination
  - STRONG BUY opportunities section highlighting best trades
  - Stock detail modal with projections, confidence, risk assessment
  - Search and filter functionality
  - Mobile-responsive design
- **FastAPI Backend**:
  - `/api/market/overview` - Market statistics and index breakdown
  - `/api/market/movers` - Top gainers and losers
  - `/api/projections/summary` - Projections overview and sentiment
  - `/api/projections/opportunities` - Filtered buy/sell opportunities
  - `/api/stocks/{symbol}` - Detailed stock information
  - `/api/stocks/{symbol}/historical` - Historical price data
  - Auto-generated API documentation (Swagger/ReDoc)
  - CORS support for local development
  - Data caching and optimization
- **React Frontend**:
  - TypeScript for type safety
  - TailwindCSS for modern styling
  - Recharts for data visualization
  - Headless UI for accessible modals
  - Custom hooks for data fetching
  - Responsive design for all screen sizes
- **Developer Tools**:
  - Startup scripts for Windows (`.bat`) and Unix (`.sh`)
  - Comprehensive dashboard documentation
  - Vite for fast development and builds

### Changed

- Updated main README with dashboard quick start
- Enhanced project structure with dashboard folder

## [0.2.0] - 2026-01-07

### Added

- **Stock Projection System**: Comprehensive 5-day price projection and recommendation engine
  - Technical analysis with momentum and volatility calculations
  - Bullish/bearish trend classification
  - Price targets (high/mid/low) with confidence scores
  - Risk assessment (Low/Medium/High)
  - Actionable recommendations (STRONG BUY to STRONG SELL)
- **Markdown Report Generation**: Human-readable projection reports for product teams
- **Projection CLI Display**: Enhanced console output with top buy/sell opportunities
- **Comprehensive Test Suite**: Unit tests for projection system
- **Documentation**: Technical documentation for stock projections feature
- **Markdown Linting**: Automated quality assurance for all markdown files

### Changed

- Enhanced data storage to support projection data in CSV and Markdown formats
- Updated workflow to integrate projection generation
- Made OpenAI dependency optional (moved to extras_require)

### Fixed

- Various markdown linting issues across documentation files

## [0.1.0] - 2026-01-02

### Added

- Initial release
- Stock screening for S&P 500 and NASDAQ-100
- Real-time data fetching via Finnhub API
- Daily market analysis with top gainers/losers
- Index comparison (SPY, QQQ)
- CSV and JSON data export
- Optional AI-powered summaries (OpenAI integration)
- Command-line interface
- Docker support
- Kubernetes CronJob configuration
- GitHub Actions for daily automated runs
- Comprehensive logging system
