# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned for v0.3.0

- **Web Dashboard**: Modern, interactive dashboard for visualizing stock data and projections
  - Real-time market overview with KPI cards
  - Interactive charts for top gainers/losers
  - Filterable stock table with detailed views
  - Historical trend analysis
  - Projection accuracy tracking
  - Mobile responsive design
  - See [Dashboard Design](docs/DASHBOARD_DESIGN.md) for full specifications

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
