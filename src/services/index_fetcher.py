"""
Stock Exchange Tracker - Index Fetcher Module

Fetches all stocks from major market indices using Python packages.
Uses pytickersymbols package for reliable, maintained index lists.
"""

from typing import List, Dict, Optional
from pathlib import Path
import json
import time
from datetime import datetime, timedelta
from ..core.logger import setup_logger

logger = setup_logger("index_fetcher")


class IndexFetcher:
    """Fetches all stocks from major market indices."""
    
    def __init__(self, cache_dir: str = "data/cache"):
        """
        Initialize index fetcher with caching.
        Uses pytickersymbols package for index constituents.
        
        Args:
            cache_dir: Directory to store cached index lists
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.cache_duration = timedelta(days=7)  # Cache for 7 days
        
        # Initialize pytickersymbols package
        try:
            from pytickersymbols import PyTickerSymbols
            self.ticker_symbols = PyTickerSymbols()
            self.package_available = True
            logger.debug("pytickersymbols package loaded successfully")
        except ImportError:
            self.ticker_symbols = None
            self.package_available = False
            logger.warning("pytickersymbols package not found. Install with: pip install pytickersymbols")
    
    def _get_minimal_fallback(self, index_name: str) -> List[str]:
        """Get minimal fallback list (only used if package and Wikipedia both fail)."""
        fallbacks = {
            "S&P 500": ["AAPL", "MSFT", "AMZN", "NVDA", "GOOGL", "META", "TSLA", "BRK.B", "V", "UNH"],
            "NASDAQ-100": ["AAPL", "MSFT", "AMZN", "NVDA", "GOOGL", "META", "TSLA", "AVGO", "COST", "NFLX"],
            "Dow Jones": ["AAPL", "MSFT", "UNH", "GS", "HD", "CAT", "MCD", "V", "HON", "TRV"]
        }
        return fallbacks.get(index_name, [])
    
    def _load_from_cache(self, index_name: str) -> Optional[List[str]]:
        """Load index symbols from cache if available and fresh."""
        cache_file = self.cache_dir / f"{index_name.replace(' ', '_').replace('&', '').replace('-', '_')}_symbols.json"
        
        if cache_file.exists():
            try:
                with open(cache_file, 'r') as f:
                    cache_data = json.load(f)
                    cached_date = datetime.fromisoformat(cache_data['date'])
                    
                    if datetime.now() - cached_date < self.cache_duration:
                        logger.debug(f"Loaded {index_name} symbols from cache ({len(cache_data['symbols'])} symbols)")
                        return cache_data['symbols']
            except Exception as e:
                logger.debug(f"Failed to load cache: {e}")
        
        return None
    
    def _save_to_cache(self, index_name: str, symbols: List[str]):
        """Save index symbols to cache."""
        cache_file = self.cache_dir / f"{index_name.replace(' ', '_').replace('&', '').replace('-', '_')}_symbols.json"
        
        try:
            cache_data = {
                'date': datetime.now().isoformat(),
                'symbols': symbols
            }
            with open(cache_file, 'w') as f:
                json.dump(cache_data, f)
            logger.debug(f"Cached {index_name} symbols ({len(symbols)} symbols)")
        except Exception as e:
            logger.warning(f"Failed to save cache: {e}")
    
    # Wikipedia scraping removed - we use pytickersymbols package only
    
    def get_sp500_symbols(self) -> List[str]:
        """
        Get all S&P 500 stock symbols using pytickersymbols package.
        """
        # Try cache first
        cached = self._load_from_cache("S&P 500")
        if cached:
            return cached
        
        # Use pytickersymbols package
        if self.package_available:
            try:
                logger.info("Fetching S&P 500 symbols from pytickersymbols package...")
                stocks = list(self.ticker_symbols.get_stocks_by_index('S&P 500'))
                symbols = [stock.get('symbol') for stock in stocks if stock.get('symbol')]
                
                if symbols and len(symbols) > 400:  # Sanity check
                    self._save_to_cache("S&P 500", symbols)
                    logger.info(f"Fetched {len(symbols)} S&P 500 symbols from package")
                    return symbols
                else:
                    logger.warning(f"Package returned unexpected data: {len(symbols)} symbols")
            except Exception as e:
                logger.warning(f"Failed to fetch from package: {e}")
        
        # Fallback to static list or Wikipedia
        logger.info("Falling back to alternative source...")
        updated = self._update_from_wikipedia("S&P 500")
        if updated and len(updated) > 400:
            self._save_to_cache("S&P 500", updated)
            return updated
        
        # Last resort: minimal fallback list
        logger.warning("Using minimal fallback list - package and Wikipedia both failed")
        fallback_list = self._get_minimal_fallback("S&P 500")
        return fallback_list
    
    def get_nasdaq100_symbols(self) -> List[str]:
        """Get all NASDAQ-100 stock symbols using pytickersymbols package."""
        cached = self._load_from_cache("NASDAQ-100")
        if cached:
            return cached
        
        # Use pytickersymbols package
        if self.package_available:
            try:
                logger.info("Fetching NASDAQ-100 symbols from pytickersymbols package...")
                stocks = list(self.ticker_symbols.get_stocks_by_index('NASDAQ 100'))
                symbols = [stock.get('symbol') for stock in stocks if stock.get('symbol')]
                
                if symbols and len(symbols) > 90:
                    self._save_to_cache("NASDAQ-100", symbols)
                    logger.info(f"Fetched {len(symbols)} NASDAQ-100 symbols from package")
                    return symbols
            except Exception as e:
                logger.warning(f"Failed to fetch from package: {e}")
        
        # Fallback
        updated = self._update_from_wikipedia("NASDAQ-100")
        if updated and len(updated) > 90:
            self._save_to_cache("NASDAQ-100", updated)
            return updated
        
        fallback_list = self._get_minimal_fallback("NASDAQ-100")
        return fallback_list
    
    def get_dow30_symbols(self) -> List[str]:
        """Get all Dow Jones Industrial Average (30 stocks) symbols using pytickersymbols package."""
        cached = self._load_from_cache("Dow Jones")
        if cached:
            return cached
        
        # Use pytickersymbols package
        if self.package_available:
            try:
                logger.info("Fetching Dow 30 symbols from pytickersymbols package...")
                # Try different index name variations
                for index_name_variant in ['DOW JONES', 'Dow Jones', 'DJIA']:
                    try:
                        stocks = list(self.ticker_symbols.get_stocks_by_index(index_name_variant))
                        symbols = [stock.get('symbol') for stock in stocks if stock.get('symbol')]
                        if symbols and len(symbols) >= 30:
                            break
                    except:
                        continue
                
                if symbols and len(symbols) >= 30:
                    self._save_to_cache("Dow Jones", symbols)
                    logger.info(f"Fetched {len(symbols)} Dow 30 symbols from package")
                    return symbols
            except Exception as e:
                logger.warning(f"Failed to fetch from package: {e}")
        
        # Fallback
        updated = self._update_from_wikipedia("Dow Jones")
        if updated and len(updated) >= 30:
            self._save_to_cache("Dow Jones", updated)
            return updated
        
        fallback_list = self._get_minimal_fallback("Dow Jones")
        return fallback_list
    
    def get_index_symbols(self, index_name: str) -> List[str]:
        """
        Get all symbols for a given index.
        
        Args:
            index_name: Name of the index (S&P 500, NASDAQ-100, Dow Jones)
        
        Returns:
            List of stock symbols
        """
        index_name_upper = index_name.upper()
        
        if "S&P" in index_name_upper or "SP500" in index_name_upper or "SP 500" in index_name_upper:
            return self.get_sp500_symbols()
        elif "NASDAQ" in index_name_upper and "100" in index_name_upper:
            return self.get_nasdaq100_symbols()
        elif "DOW" in index_name_upper or "DJIA" in index_name_upper:
            return self.get_dow30_symbols()
        else:
            logger.warning(f"Unknown index: {index_name}")
            return []
