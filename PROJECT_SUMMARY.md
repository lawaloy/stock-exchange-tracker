# Stock Exchange Tracker - Project Summary

## Overview

A professional, production-ready stock market tracking tool that automatically identifies promising stocks, fetches real-time market data, and generates insights using official APIs.

**Current Version**: 1.0.0  
**Status**: ✅ Production Ready  
**Run Time**: ~4 minutes per day  
**API Calls**: ~241 (optimized for free tier)

---

## Project Structure

```
stock-exchange-tracker/
├── README.md                    # Main documentation
├── CHANGELOG.md                 # Version history
├── CONTRIBUTING.md              # Contribution guidelines
├── LICENSE                      # MIT License
├── requirements.txt             # Python dependencies
├── setup.cfg                    # Package configuration
├── pytest.ini                   # Test configuration
├── Dockerfile                   # Container image
├── main.py                      # Entry point
│
├── config/                      # User configuration
│   ├── exchanges.json           # Indices to track
│   └── filters.json             # Screening criteria
│
├── src/                         # Source code (modular)
│   ├── core/                    # Core utilities
│   │   ├── config.py            # Configuration loader
│   │   └── logger.py            # Logging setup
│   ├── services/                # External services
│   │   ├── api_client.py        # Finnhub API client
│   │   ├── data_fetcher.py      # Data orchestration
│   │   ├── index_fetcher.py     # Index symbols
│   │   └── stock_screener.py    # Stock screening
│   ├── analysis/                # Analysis & AI
│   │   ├── analyzer.py          # Statistical analysis
│   │   └── ai_summarizer.py     # AI summaries
│   ├── storage/                 # Data persistence
│   │   └── data_storage.py      # CSV/JSON storage
│   └── cli/                     # CLI interface
│       └── stock_tracker.py     # Main workflow
│
├── tests/                       # Test suite
│   ├── test_core_config.py
│   ├── test_core_logger.py
│   ├── test_services_api_client.py
│   ├── test_analysis_analyzer.py
│   ├── test_storage.py
│   └── README.md
│
├── k8s/                         # Kubernetes manifests
│   └── stock-tracker-cronjob.yaml
│
├── data/                        # Output (gitignored)
│   ├── daily_data_*.csv
│   ├── summary_*.json
│   └── cache/
│
└── logs/                        # Logs (gitignored)
    ├── stock_tracker_*.log
    └── stock_tracker_errors_*.log
```

---

## Key Features

### ✅ Production-Ready Architecture
- Modular design with clear separation of concerns
- Professional error handling and logging
- Comprehensive test suite
- Docker support with Kubernetes manifests
- CI/CD ready (GitHub Actions)

### ✅ Optimized Performance
- **44% reduction** in API calls (431 → 241)
- **50% faster** run time (7-8 min → 4 min)
- Thread-safe rate limiting
- Efficient parallel processing
- Smart caching for index symbols

### ✅ Official APIs Only
- **Finnhub API** for stock data (no scraping)
- **pytickersymbols** for index constituents
- **OpenAI API** for AI summaries (optional)
- Robust retry logic and error handling

### ✅ Flexible Configuration
- Dynamic stock discovery (no hardcoded lists)
- Configurable screening filters
- Weighted scoring system
- Customizable indices to track

---

## Technical Highlights

### API Optimization
```
Screening Phase:
  - S&P 500: 100 stocks × 1 call = 100 calls
  - NASDAQ-100: 101 stocks × 1 call = 101 calls
  Subtotal: 201 calls

Full Fetch Phase:
  - Top 20 stocks × 2 calls = 40 calls
  Subtotal: 40 calls

Total: 241 calls (~4 minutes)
```

### Rate Limiting
- Token bucket algorithm (thread-safe)
- 60 calls/minute (Finnhub free tier)
- Automatic retry with exponential backoff
- Explicit 429 error handling
- Rolling minute budget enforcement

### Data Quality
- Real-time quotes from official API
- Company profiles (name, market cap)
- Daily change calculations
- Volume and price metrics
- Configurable screening criteria

---

## Quick Start

```bash
# 1. Clone and install
git clone https://github.com/lawaloy/stock-exchange-tracker.git
cd stock-exchange-tracker
pip install -e .

# 2. Configure API key
echo "FINNHUB_API_KEY=your-key-here" > .env

# 3. Run
python main.py
```

---

## Deployment Options

### Local Development
```bash
python main.py
```

### Docker
```bash
docker build -t stock-tracker .
docker run --rm -e FINNHUB_API_KEY=your-key stock-tracker
```

### Kubernetes
```bash
kubectl create secret generic api-keys --from-literal=FINNHUB_API_KEY=your-key
kubectl apply -f k8s/stock-tracker-cronjob.yaml
```

### GitHub Actions
- Automated daily runs
- Secrets management via GitHub
- Workflow dispatch for manual runs

---

## Testing

```bash
# Run all tests
python -m pytest tests/ -v

# With coverage
python -m pytest tests/ --cov=src --cov-report=html

# Specific module
python -m pytest tests/test_core_config.py -v
```

**Current Coverage:**
- Core: Configuration, logging
- Services: API client, rate limiting
- Analysis: Statistical analysis
- Storage: Data persistence

---

## Configuration

### Indices to Track (`config/exchanges.json`)
```json
{
  "indices_to_track": ["S&P 500", "NASDAQ-100"]
}
```

### Screening Filters (`config/filters.json`)
```json
{
  "volume_threshold": 1000000,
  "price_min": 5.0,
  "price_max": 500.0,
  "min_daily_change_pct": 2.0,
  "market_cap_min": 1000000000,
  "top_n": 20
}
```

---

## Output

### Daily Data CSV
```
symbol,date,open,close,high,low,volume,previous_close,change,change_percent,name,exchange,market_cap
AAPL,2026-01-04,150.0,152.5,153.0,149.5,50000000,148.0,4.5,3.04,Apple Inc,NASDAQ,2500000000000
...
```

### Summary JSON
```json
{
  "date": "2026-01-04",
  "total_stocks": 20,
  "gainers_count": 15,
  "losers_count": 5,
  "top_gainers": [...],
  "top_losers": [...],
  "index_comparison": {...}
}
```

---

## Dependencies

**Core:**
- Python 3.12+
- pandas
- requests
- python-dotenv

**APIs:**
- Finnhub (stock data)
- pytickersymbols (index constituents)
- OpenAI (optional, for AI summaries)

**Development:**
- pytest
- pytest-cov

---

## Security

✅ API keys stored in `.env` (gitignored)  
✅ Secrets management for production  
✅ No hardcoded credentials  
✅ Secure Docker/K8s deployment patterns  
✅ Regular key rotation recommended  

---

## Performance Metrics

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| API Calls | 431 | 241 | -44% |
| Run Time | 7-8 min | 4 min | -50% |
| Stocks Screened | 251 | 201 | -20% |
| Top Stocks | 30 | 20 | Focused |
| Calls per Stock | 3 | 2 | -33% |

---

## Roadmap

### v1.1.0 (Planned)
- [ ] Enhanced test coverage (integration tests)
- [ ] Performance benchmarking
- [ ] Additional exchange support
- [ ] Data visualization

### Future Considerations
- [ ] Web dashboard
- [ ] Historical analysis
- [ ] Backtesting
- [ ] Alert system
- [ ] Multi-currency support

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Areas for Contribution:**
- Additional tests
- Performance optimizations
- New features
- Documentation improvements

---

## License

MIT License - See [LICENSE](LICENSE) for details.

---

## Support

- **Issues**: [GitHub Issues](https://github.com/lawaloy/stock-exchange-tracker/issues)
- **Discussions**: [GitHub Discussions](https://github.com/lawaloy/stock-exchange-tracker/discussions)
- **Documentation**: [README.md](README.md)

---

## Acknowledgments

- **Finnhub** for providing free stock market API
- **pytickersymbols** for index constituent data
- **OpenAI** for AI-powered summaries

---

**Built with ❤️ by lawaloy**

Last Updated: 2026-01-04

