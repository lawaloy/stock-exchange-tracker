"""Tests for storage module."""

import unittest
import tempfile
import shutil
from pathlib import Path
import pandas as pd
import json
from datetime import date

from src.storage.data_storage import DataStorage


class TestDataStorage(unittest.TestCase):
    """Test cases for data storage."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_data_dir = tempfile.mkdtemp()
        self.storage = DataStorage(data_dir=self.test_data_dir)
        self.sample_df = pd.DataFrame({
            'symbol': ['AAPL', 'GOOGL'],
            'close': [150.0, 2800.0],
            'volume': [50000000, 30000000]
        })
        self.sample_summary = {
            'total_stocks': 2,
            'date': str(date.today())
        }

    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_data_dir, ignore_errors=True)

    def test_storage_initialization(self):
        """Test that storage initializes correctly."""
        self.assertIsInstance(self.storage, DataStorage)
        self.assertTrue(Path(self.test_data_dir).exists())

    def test_save_daily_data(self):
        """Test saving daily data to CSV."""
        data_list = self.sample_df.to_dict('records')
        self.storage.save_daily_data(data_list)
        csv_files = list(Path(self.test_data_dir).glob("daily_data_*.csv"))
        self.assertEqual(len(csv_files), 1)

    def test_save_summary(self):
        """Test saving summary to JSON."""
        self.storage.save_summary(self.sample_summary)
        json_files = list(Path(self.test_data_dir).glob("summary_*.json"))
        self.assertEqual(len(json_files), 1)

    def test_load_daily_data(self):
        """Test loading daily data from CSV."""
        data_list = self.sample_df.to_dict('records')
        self.storage.save_daily_data(data_list)
        loaded_df = self.storage.load_daily_data()
        self.assertIsInstance(loaded_df, pd.DataFrame)
        self.assertEqual(len(loaded_df), 2)
        self.assertIn('symbol', loaded_df.columns)

    def test_load_summary(self):
        """Test loading summary from JSON."""
        self.storage.save_summary(self.sample_summary)
        json_files = list(Path(self.test_data_dir).glob("summary_*.json"))
        self.assertEqual(len(json_files), 1)
        with open(json_files[0], 'r') as f:
            loaded_summary = json.load(f)
        self.assertIsInstance(loaded_summary, dict)
        self.assertEqual(loaded_summary['total_stocks'], 2)


if __name__ == '__main__':
    unittest.main()
