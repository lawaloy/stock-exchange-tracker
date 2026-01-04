"""Tests for analysis analyzer module."""

import unittest
import pandas as pd
from datetime import date
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.analysis.analyzer import StockAnalyzer


class TestStockAnalyzer(unittest.TestCase):
    """Test cases for stock analyzer."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.analyzer = StockAnalyzer()
        
        # Create sample stock data
        self.sample_data = pd.DataFrame({
            'symbol': ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'AMZN'],
            'date': [date.today()] * 5,
            'close': [150.0, 2800.0, 300.0, 200.0, 3200.0],
            'previous_close': [148.0, 2750.0, 298.0, 205.0, 3150.0],
            'change': [2.0, 50.0, 2.0, -5.0, 50.0],
            'change_percent': [1.35, 1.82, 0.67, -2.44, 1.59],
            'volume': [50000000, 30000000, 40000000, 60000000, 35000000],
            'market_cap': [2500000000000, 1800000000000, 2300000000000, 600000000000, 1600000000000],
            'name': ['Apple Inc', 'Alphabet Inc', 'Microsoft', 'Tesla', 'Amazon'],
            'exchange': ['NASDAQ'] * 5
        })
    
    def test_analyzer_initialization(self):
        """Test that analyzer initializes correctly."""
        self.assertIsInstance(self.analyzer, StockAnalyzer)
    
    def test_analyze_returns_dict(self):
        """Test that analyze returns a dictionary."""
        # Convert DataFrame to list of dicts for the actual API
        data_list = self.sample_data.to_dict('records')
        result = self.analyzer.analyze_daily_data(data_list)
        
        self.assertIsInstance(result, dict)
    
    def test_analyze_has_top_gainers(self):
        """Test that analysis includes top gainers."""
        data_list = self.sample_data.to_dict('records')
        result = self.analyzer.analyze_daily_data(data_list)
        
        self.assertIn('top_gainers', result)
        gainers = result['top_gainers']
        self.assertGreater(len(gainers), 0)
        
        # Top gainer should be GOOGL (1.82%)
        self.assertEqual(gainers[0]['symbol'], 'GOOGL')
    
    def test_analyze_has_top_losers(self):
        """Test that analysis includes top losers."""
        data_list = self.sample_data.to_dict('records')
        result = self.analyzer.analyze_daily_data(data_list)
        
        self.assertIn('top_losers', result)
        losers = result['top_losers']
        self.assertGreater(len(losers), 0)
        
        # Top loser should be TSLA (-2.44%)
        self.assertEqual(losers[0]['symbol'], 'TSLA')
    
    def test_analyze_has_statistics(self):
        """Test that analysis includes statistics."""
        data_list = self.sample_data.to_dict('records')
        result = self.analyzer.analyze_daily_data(data_list)
        
        # Check for 'summary' key which contains the statistics
        self.assertIn('summary', result)
        summary = result['summary']
        
        self.assertIn('total_stocks', summary)
        self.assertIn('gainers', summary)
        self.assertIn('losers', summary)
        self.assertIn('average_change_percent', summary)
        
        self.assertEqual(summary['total_stocks'], 5)
        self.assertEqual(summary['gainers'], 4)
        self.assertEqual(summary['losers'], 1)
    
    def test_empty_dataframe(self):
        """Test handling of empty dataframe."""
        empty_data = []
        result = self.analyzer.analyze_daily_data(empty_data)
        
        # Empty data returns an empty dict
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), 0)


if __name__ == '__main__':
    unittest.main()

