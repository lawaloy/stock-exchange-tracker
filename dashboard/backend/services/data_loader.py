"""
Data loading service for reading CSV and JSON files
"""
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import pandas as pd
import json
from datetime import datetime, timedelta
from functools import lru_cache


class DataLoader:
    """Loads and caches stock market data from CSV/JSON files"""
    
    def __init__(self, data_dir: Optional[Path] = None):
        if data_dir is None:
            # Default to data directory in project root
            self.data_dir = Path(__file__).parent.parent.parent.parent / "data"
        else:
            self.data_dir = Path(data_dir)
        
        if not self.data_dir.exists():
            raise ValueError(f"Data directory not found: {self.data_dir}")
    
    def _get_latest_file(self, pattern: str, sort_by_date: bool = False) -> Optional[Path]:
        """Get the most recent file matching the pattern.
        When sort_by_date=True, uses date in filename (YYYY-MM-DD) for daily_data/projections/summary.
        """
        files = list(self.data_dir.glob(pattern))
        if not files:
            return None
        if sort_by_date:
            # Extract date from filename (e.g. daily_data_2026-02-14.csv) and pick latest
            def parse_date(f: Path) -> str:
                stem = f.stem
                if "daily_data_" in stem:
                    return stem.replace("daily_data_", "")
                if "projections_" in stem:
                    return stem.replace("projections_", "")
                if "summary_" in stem:
                    return stem.replace("summary_", "")
                return ""
            dated = [(f, parse_date(f)) for f in files if parse_date(f)]
            if not dated:
                return max(files, key=lambda f: f.stat().st_mtime)
            dated.sort(key=lambda x: x[1], reverse=True)
            return dated[0][0]
        return max(files, key=lambda f: f.stat().st_mtime)

    def get_latest_date(self) -> Optional[str]:
        """Get the date of the most recent data (by date in filename, not file mtime)"""
        dates = self.get_available_dates()
        return dates[0] if dates else None
    
    def load_daily_data(self, date: Optional[str] = None) -> pd.DataFrame:
        """Load daily stock data CSV"""
        if date is None:
            file_path = self._get_latest_file("daily_data_*.csv", sort_by_date=True)
            if file_path is None:
                raise ValueError("No daily data files found")
        else:
            file_path = self.data_dir / f"daily_data_{date}.csv"
            if not file_path.exists():
                raise ValueError(f"Daily data file not found for date: {date}")
        
        df = pd.read_csv(file_path)
        return df
    
    def load_projections(self, date: Optional[str] = None) -> pd.DataFrame:
        """Load projections CSV"""
        if date is None:
            file_path = self._get_latest_file("projections_*.csv", sort_by_date=True)
            if file_path is None:
                raise ValueError("No projection files found")
        else:
            file_path = self.data_dir / f"projections_{date}.csv"
            if not file_path.exists():
                raise ValueError(f"Projections file not found for date: {date}")
        
        df = pd.read_csv(file_path)
        return df
    
    def load_summary(self, date: Optional[str] = None) -> Dict:
        """Load summary JSON"""
        if date is None:
            file_path = self._get_latest_file("summary_*.json", sort_by_date=True)
            if file_path is None:
                raise ValueError("No summary files found")
        else:
            file_path = self.data_dir / f"summary_{date}.json"
            if not file_path.exists():
                raise ValueError(f"Summary file not found for date: {date}")
        
        with open(file_path, 'r') as f:
            return json.load(f)
    
    def get_available_dates(self) -> List[str]:
        """Get list of all available dates"""
        files = list(self.data_dir.glob("daily_data_*.csv"))
        dates = [f.stem.replace("daily_data_", "") for f in files]
        return sorted(dates, reverse=True)
    
    def load_historical_data(self, symbol: str, days: int = 30) -> List[Dict]:
        """Load historical data for a specific symbol"""
        dates = self.get_available_dates()
        cutoff_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        
        historical_data = []
        for date in dates:
            if date < cutoff_date:
                break
            
            try:
                # Load daily data
                daily_df = self.load_daily_data(date)
                stock_data = daily_df[daily_df['symbol'] == symbol]
                
                if stock_data.empty:
                    continue
                
                stock_record = stock_data.iloc[0].to_dict()
                
                # Try to load projections for this date
                try:
                    proj_df = self.load_projections(date)
                    proj_data = proj_df[proj_df['symbol'] == symbol]
                    
                    if not proj_data.empty:
                        proj_record = proj_data.iloc[0].to_dict()
                        stock_record['projection'] = {
                            'target_price': proj_record.get('target_mid', None),
                            'confidence': proj_record.get('confidence', None),
                            'recommendation': proj_record.get('recommendation', None),
                            'expected_change': proj_record.get('expected_change_percent', None)
                        }
                except Exception:
                    # No projection data for this date
                    pass
                
                stock_record['date'] = date
                historical_data.append(stock_record)
            
            except Exception:
                continue
        
        return historical_data


# Singleton instance with caching
_data_loader = None


def get_data_loader() -> DataLoader:
    """Get the singleton DataLoader instance"""
    global _data_loader
    if _data_loader is None:
        _data_loader = DataLoader()
    return _data_loader
