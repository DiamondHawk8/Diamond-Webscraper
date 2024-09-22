# test_scraper.py

import unittest
from scraper import WebScraper, calculate_backoff
from unittest.mock import patch
import requests
import logging
from requests.models import Response
import random

class TestWebScraper(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Configure logging once for all tests
        logging.basicConfig(
            filename='test_scraper.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
        )
        logging.info("\n========== Starting WebScraper Tests ==========")

    @patch('requests.get')
    def test_fetch_content_success(self, mock_get):
        logging.info("========== Starting: test_fetch_content_success ==========")

        # Create a mock response object
        mock_response = Response()
        mock_response.status_code = 200
        mock_response._content = b'<html><body>Test</body></html>'

        mock_get.return_value = mock_response

        scraper = WebScraper(base_url="https://example.com", headers={}, timeout=10)
        content = scraper.fetch_content()

        # Validate that the content is fetched correctly
        self.assertIsNotNone(content)
        self.assertIn('Test', content)

        logging.info("Completed: test_fetch_content_success")

    @patch('requests.get')
    def test_fetch_content_failure(self, mock_get):
        logging.info("========== Starting: test_fetch_content_failure ==========")

        # Mock requests.get to raise a RequestException
        mock_get.side_effect = requests.exceptions.RequestException("Test exception")

        scraper = WebScraper(base_url="https://example.com", headers={}, timeout=10)
        content = scraper.fetch_content()

        # Check if fetch_content handled error properly and returned None
        self.assertIsNone(content)

        logging.info("Completed: test_fetch_content_failure")

    def test_parse_content(self):
        logging.info("========== Starting: test_parse_content ==========")

        # Test parse_content method with sample HTML
        html_content = '<html><body><a href="https://link1.com">Link1</a></body></html>'
        scraper = WebScraper(base_url="https://example.com", headers={}, timeout=10)
        parsed_data = scraper.parse_content(html_content)

        # Validate that the correct link is extracted
        self.assertIn('https://link1.com', parsed_data)

        logging.info("Completed: test_parse_content")

    def test_backoff_calculation(self):
        logging.info("========== Starting: test_backoff_calculation ==========")

        backoff_factor = 2
        attempt = 3

        # Mock random.uniform to return a fixed value for predictable testing
        with patch('random.uniform', return_value=0.5):
            calculated_delay = calculate_backoff(attempt, backoff_factor)

        expected_base_delay = backoff_factor * (2 ** attempt)
        expected_delay = expected_base_delay + 0.5  # Added jitter

        # Check if the calculated delay matches the expected delay
        self.assertEqual(calculated_delay, expected_delay)

        logging.info("Completed: test_backoff_calculation")

    @patch('requests.get')
    def test_exponential_backoff_integration(self, mock_get):
        logging.info("========== Starting: test_exponential_backoff_integration ==========")

        # Mock a transient error for the first two attempts, then success
        mock_get.side_effect = [
            requests.exceptions.ConnectionError("Connection error on attempt 1"),
            requests.exceptions.Timeout("Timeout on attempt 2"),
            self._mock_successful_response()
        ]

        scraper = WebScraper(base_url="https://example.com", headers={}, timeout=10)

        # Mock time.sleep to avoid actual delays during testing
        with patch('time.sleep', return_value=None):
            content = scraper.fetch_content(max_retries=3, backoff_factor=1)

        # Ensure that the content is eventually fetched
        self.assertIsNotNone(content)
        self.assertIn('Test', content)

        logging.info("Completed: test_exponential_backoff_integration")

    def _mock_successful_response(self):
        """Helper method to create a successful mock response."""
        mock_response = Response()
        mock_response.status_code = 200
        mock_response._content = b'<html><body>Test</body></html>'
        return mock_response

    @classmethod
    def tearDownClass(cls):
        logging.info("\n========== Completed WebScraper Tests ==========")

if __name__ == '__main__':
    unittest.main()
