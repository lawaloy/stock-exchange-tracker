"""
Stock Exchange Tracker - Data Storage Module

Handles saving and loading stock market data to/from CSV files.
"""

import pandas as pd
import os
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from pathlib import Path


class DataStorage:
    """Manages storage of stock market data in CSV format."""
    
    def __init__(self, data_dir: str = "data"):
        """
        Initialize data storage.
        
        Args:
            data_dir: Directory to store data files
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
    
    def _get_daily_file_path(self, date: datetime.date = None) -> Path:
        """Get file path for daily data."""
        if date is None:
            date = datetime.now().date()
        
        filename = f"daily_data_{date.strftime('%Y-%m-%d')}.csv"
        return self.data_dir / filename
    
    def save_daily_data(self, data: List[Dict], date: datetime.date = None) -> str:
        """
        Save daily stock data to CSV.
        
        Args:
            data: List of stock data dictionaries
            date: Date for the data (defaults to today)
        
        Returns:
            Path to saved file
        """
        if not data:
            return None
        
        df = pd.DataFrame(data)
        file_path = self._get_daily_file_path(date)
        df.to_csv(file_path, index=False)
        return str(file_path)
    
    def load_daily_data(self, date: datetime.date = None) -> Optional[pd.DataFrame]:
        """
        Load daily stock data from CSV.
        
        Args:
            date: Date to load (defaults to today)
        
        Returns:
            DataFrame with stock data or None if not found
        """
        file_path = self._get_daily_file_path(date)
        
        if not file_path.exists():
            return None
        
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            print(f"Error loading data from {file_path}: {str(e)}")
            return None
    
    def save_summary(self, summary_data: Dict, date: datetime.date = None) -> str:
        """
        Save daily summary statistics.
        
        Args:
            summary_data: Dictionary with summary statistics
            date: Date for the summary (defaults to today)
        
        Returns:
            Path to saved file
        """
        if date is None:
            date = datetime.now().date()
        
        summary_path = self.data_dir / f"summary_{date.strftime('%Y-%m-%d')}.json"
        
        summary_data["date"] = str(date)
        with open(summary_path, 'w') as f:
            json.dump(summary_data, f, indent=2)
        
        return str(summary_path)
    
    def get_historical_data(self, start_date: datetime.date = None, 
                          end_date: datetime.date = None) -> pd.DataFrame:
        """
        Load historical data for a date range.
        
        Args:
            start_date: Start date (defaults to 30 days ago)
            end_date: End date (defaults to today)
        
        Returns:
            Combined DataFrame with historical data
        """
        if end_date is None:
            end_date = datetime.now().date()
        if start_date is None:
            start_date = end_date - timedelta(days=30)
        
        all_data = []
        current_date = start_date
        
        while current_date <= end_date:
            df = self.load_daily_data(current_date)
            if df is not None and not df.empty:
                all_data.append(df)
            current_date += timedelta(days=1)
        
        if all_data:
            return pd.concat(all_data, ignore_index=True)
        return pd.DataFrame()

