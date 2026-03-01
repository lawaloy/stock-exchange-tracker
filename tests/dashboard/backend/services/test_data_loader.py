"""Tests for dashboard data loader service."""

import os
import tempfile
import shutil
import json
import time
import pandas as pd
from pathlib import Path

import pytest


@pytest.fixture
def temp_data_dir():
    """Create temp data directory."""
    tmp = tempfile.mkdtemp()
    yield Path(tmp)
    shutil.rmtree(tmp, ignore_errors=True)


@pytest.fixture
def loader(temp_data_dir):
    """Create DataLoader with temp directory."""
    from dashboard.backend.services.data_loader import DataLoader
    return DataLoader(data_dir=temp_data_dir)


class TestDataLoader:
    """Test DataLoader class."""

    def test_raises_for_missing_data_dir(self):
        """DataLoader raises when data directory does not exist."""
        from dashboard.backend.services.data_loader import DataLoader

        with pytest.raises(ValueError, match="Data directory not found"):
            DataLoader(data_dir=Path("/nonexistent/path"))

    def test_get_latest_date_returns_none_when_empty(self, loader):
        """get_latest_date returns None when no daily data files."""
        assert loader.get_latest_date() is None

    def test_load_daily_data_raises_when_no_files(self, loader):
        """load_daily_data raises when no files exist."""
        with pytest.raises(ValueError, match="No daily data files found"):
            loader.load_daily_data()

    def test_load_summary_raises_when_no_files(self, loader):
        """load_summary raises when no summary files exist."""
        with pytest.raises(ValueError, match="No summary files found"):
            loader.load_summary()

    def test_load_daily_data_returns_dataframe(self, loader, temp_data_dir):
        """load_daily_data returns correct DataFrame."""
        df = pd.DataFrame({
            "symbol": ["AAPL", "GOOGL"],
            "close": [150.0, 2800.0],
            "change_percent": [1.0, -0.5],
        })
        df.to_csv(temp_data_dir / "daily_data_2026-01-15.csv", index=False)

        result = loader.load_daily_data()
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2
        assert "symbol" in result.columns

    def test_load_summary_returns_dict(self, loader, temp_data_dir):
        """load_summary returns correct dict."""
        summary = {"date": "2026-01-15", "analysis": {}}
        with open(temp_data_dir / "summary_2026-01-15.json", "w") as f:
            json.dump(summary, f)

        result = loader.load_summary()
        assert isinstance(result, dict)
        assert result["date"] == "2026-01-15"

    def test_get_latest_date_returns_date_string(self, loader, temp_data_dir):
        """get_latest_date returns date from most recent file by filename date."""
        df = pd.DataFrame({"symbol": ["A"], "close": [100.0], "change_percent": [0.0]})
        df.to_csv(temp_data_dir / "daily_data_2026-01-20.csv", index=False)
        df.to_csv(temp_data_dir / "daily_data_2026-01-15.csv", index=False)

        result = loader.get_latest_date()
        assert result == "2026-01-20"

    def test_get_latest_date_uses_filename_date_not_mtime(self, loader, temp_data_dir):
        """get_latest_date uses date in filename, not file mtime."""
        df = pd.DataFrame({"symbol": ["A"], "close": [100.0], "change_percent": [0.0]})
        newer_date_file = temp_data_dir / "daily_data_2026-01-20.csv"
        older_date_file = temp_data_dir / "daily_data_2026-01-15.csv"
        df.to_csv(newer_date_file, index=False)
        df.to_csv(older_date_file, index=False)
        # Make older-date file have newer mtime
        time.sleep(0.01)
        os.utime(older_date_file, (time.time(), time.time()))

        result = loader.get_latest_date()
        assert result == "2026-01-20"

    def test_get_available_dates_returns_sorted_list(self, loader, temp_data_dir):
        """get_available_dates returns sorted list of dates."""
        df = pd.DataFrame({"symbol": ["A"], "close": [100.0], "change_percent": [0.0]})
        df.to_csv(temp_data_dir / "daily_data_2026-01-10.csv", index=False)
        df.to_csv(temp_data_dir / "daily_data_2026-01-15.csv", index=False)

        result = loader.get_available_dates()
        assert len(result) == 2
        assert result == sorted(result, reverse=True)

    def test_load_daily_data_loads_by_filename_date_not_mtime(self, loader, temp_data_dir):
        """load_daily_data loads latest by date in filename, not mtime."""
        df_old = pd.DataFrame({"symbol": ["OLD"], "close": [50.0], "change_percent": [0.0]})
        df_new = pd.DataFrame({"symbol": ["NEW"], "close": [100.0], "change_percent": [0.0]})
        newer_file = temp_data_dir / "daily_data_2026-01-20.csv"
        older_file = temp_data_dir / "daily_data_2026-01-15.csv"
        df_new.to_csv(newer_file, index=False)
        df_old.to_csv(older_file, index=False)
        time.sleep(0.01)
        os.utime(older_file, (time.time(), time.time()))

        result = loader.load_daily_data()
        assert result.iloc[0]["symbol"] == "NEW"
