"""Tests for AI summarizer module."""

from unittest.mock import patch

import pytest

from src.analysis.ai_summarizer import AISummarizer


class TestAISummarizerDemoSummary:
    """Test demo summary generation (no API key)."""

    def test_generate_demo_summary_positive_sentiment(self):
        """Demo summary with more gainers than losers shows positive sentiment."""
        summarizer = AISummarizer()
        analysis = {
            "summary": {"gainers": 5, "losers": 2, "average_change_percent": 0.5},
            "top_gainers": [{"symbol": "AAPL", "change_percent": 2.5}],
            "top_losers": [{"symbol": "GOOGL", "change_percent": -1.0}],
        }
        exchange_comparison = {"S&P 500": {"average_change_percent": 0.6}}

        result = summarizer.generate_demo_summary(analysis, exchange_comparison)

        assert "positive" in result
        assert "5 gainers" in result
        assert "2 losers" in result
        assert "AAPL" in result
        assert "GOOGL" in result
        assert "S&P 500" in result

    def test_generate_demo_summary_negative_sentiment(self):
        """Demo summary with more losers than gainers shows negative sentiment."""
        summarizer = AISummarizer()
        analysis = {
            "summary": {"gainers": 2, "losers": 6, "average_change_percent": -0.8},
            "top_gainers": [{"symbol": "MSFT", "change_percent": 0.5}],
            "top_losers": [{"symbol": "META", "change_percent": -3.2}],
        }
        exchange_comparison = {"NASDAQ-100": {"average_change_percent": -0.5}}

        result = summarizer.generate_demo_summary(analysis, exchange_comparison)

        assert "negative" in result
        assert "2 gainers" in result
        assert "6 losers" in result
        assert "MSFT" in result
        assert "META" in result

    def test_generate_demo_summary_mixed_sentiment(self):
        """Demo summary with equal gainers/losers shows mixed sentiment."""
        summarizer = AISummarizer()
        analysis = {
            "summary": {"gainers": 3, "losers": 3, "average_change_percent": 0.0},
            "top_gainers": [],
            "top_losers": [],
        }
        exchange_comparison = {}

        result = summarizer.generate_demo_summary(analysis, exchange_comparison)

        assert "mixed" in result

    def test_generate_demo_summary_empty_exchange_comparison(self):
        """Demo summary works with empty exchange comparison."""
        summarizer = AISummarizer()
        analysis = {
            "summary": {"gainers": 1, "losers": 1, "average_change_percent": 0.0},
            "top_gainers": [{"symbol": "A", "change_percent": 1.0}],
            "top_losers": [{"symbol": "B", "change_percent": -1.0}],
        }
        exchange_comparison = {}

        result = summarizer.generate_demo_summary(analysis, exchange_comparison)

        assert "A" in result
        assert "B" in result

    @patch("src.analysis.ai_summarizer.os.getenv")
    def test_generate_summary_returns_demo_when_no_api_key(self, mock_getenv):
        """generate_summary returns demo summary when OPENAI_API_KEY not set."""
        import os as os_module

        def fake_getenv(key, default=None):
            if key == "OPENAI_API_KEY":
                return None
            return os_module.environ.get(key, default)

        mock_getenv.side_effect = fake_getenv
        summarizer = AISummarizer()
        analysis = {
            "summary": {"gainers": 2, "losers": 1, "average_change_percent": 0.3},
            "top_gainers": [{"symbol": "X", "change_percent": 1.0}],
            "top_losers": [{"symbol": "Y", "change_percent": -0.5}],
        }
        exchange_comparison = {}

        result = summarizer.generate_summary(analysis, exchange_comparison)

        assert result is not None
        assert "sentiment" in result.lower()
