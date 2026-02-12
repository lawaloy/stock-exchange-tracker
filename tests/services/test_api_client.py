"""Tests for services API client module."""

import unittest
from unittest.mock import Mock, patch

from src.services.api_client import RateLimiter, FinnhubClient


class TestRateLimiter(unittest.TestCase):
    """Test cases for rate limiter."""

    def test_rate_limiter_initialization(self):
        """Test rate limiter initializes correctly."""
        limiter = RateLimiter(calls_per_minute=60)
        self.assertEqual(limiter.calls_per_minute, 60)
        self.assertGreater(limiter.tokens, 0)

    def test_wait_if_needed(self):
        """Test that wait_if_needed executes without error."""
        limiter = RateLimiter(calls_per_minute=60)
        limiter.wait_if_needed()
        self.assertLess(limiter.tokens, 10)


class TestFinnhubClient(unittest.TestCase):
    """Test cases for Finnhub API client."""

    def setUp(self):
        """Set up test fixtures."""
        self.api_key = "test_api_key_12345"

    def test_client_requires_api_key(self):
        """Test that client raises error without API key."""
        with patch.dict('os.environ', {}, clear=True):
            with self.assertRaises(ValueError) as context:
                FinnhubClient(api_key=None)
            self.assertIn("API key required", str(context.exception))

    @patch('requests.Session')
    def test_client_initialization(self, mock_session):
        """Test that client initializes with API key."""
        client = FinnhubClient(api_key=self.api_key)
        self.assertEqual(client.api_key, self.api_key)
        self.assertEqual(client.base_url, "https://finnhub.io/api/v1")

    @patch('requests.Session')
    def test_get_quote_structure(self, mock_session):
        """Test get_quote returns expected structure."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "c": 150.0, "h": 152.0, "l": 149.0, "o": 151.0,
            "pc": 148.0, "t": 1234567890
        }
        mock_session_instance = Mock()
        mock_session_instance.get.return_value = mock_response
        mock_session.return_value = mock_session_instance

        client = FinnhubClient(api_key=self.api_key)
        client.session = mock_session_instance
        quote = client.get_quote("AAPL")

        self.assertIsInstance(quote, dict)
        self.assertIn("c", quote)
        self.assertIn("pc", quote)

    @patch('requests.Session')
    def test_get_stock_data_for_screening(self, mock_session):
        """Test lightweight screening data fetch."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "c": 150.0, "pc": 148.0, "v": 50000000
        }
        mock_session_instance = Mock()
        mock_session_instance.get.return_value = mock_response
        mock_session.return_value = mock_session_instance

        client = FinnhubClient(api_key=self.api_key)
        client.session = mock_session_instance
        data = client.get_stock_data_for_screening("AAPL")

        self.assertIsNotNone(data)
        self.assertEqual(data["symbol"], "AAPL")
        self.assertIn("close", data)
        self.assertIn("volume", data)
        self.assertIn("change_percent", data)


if __name__ == '__main__':
    unittest.main()
