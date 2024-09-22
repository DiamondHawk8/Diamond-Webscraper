import unittest
from scraper import WebScraper, calculate_backoff
from unittest.mock import patch
import requests
import logging

# Set up logging for the test cases
logging.basicConfig(
    filename='test_scraper.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)


class TestWebScraper(unittest.TestCase):

    @patch('requests.get')
    def test_fetch_content_success(self, mock_get):
        logging.info("\n========== Starting: test_fetch_content_success ==========")

        # Mocking a successful requests.get() response
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = '<html><body>Test</body></html>'

        scraper = WebScraper(base_url="https://example.com", headers={})
        content = scraper.fetch_content()

        # Validate that the content is fetched correctly
        self.assertIsNotNone(content)
        self.assertIn('Test', content)

        logging.info("Completed: test_fetch_content_success")

    @patch('requests.get')
    def test_fetch_content_failure(self, mock_get):
        logging.info("\n========== Starting: test_fetch_content_failure ==========")

        # Mock requests.get to raise a RequestException
        mock_get.side_effect = requests.exceptions.RequestException

        scraper = WebScraper(base_url="https://example.com", headers={})
        content = scraper.fetch_content()

        # Check if fetch content handled error properly and returned None
        self.assertIsNone(content)

        logging.info("Completed: test_fetch_content_failure")

    def test_parse_content(self):
        logging.info("\n========== Starting: test_parse_content ==========")

        # Test parse_content method with sample HTML
        html_content = '<html><body><a href="https://link1.com">Link1</a></body></html>'
        scraper = WebScraper(base_url="https://example.com", headers={})
        parsed_data = scraper.parse_content(html_content)

        # Validate that the correct link is extracted
        self.assertIn('https://link1.com', parsed_data)

        logging.info("Completed: test_parse_content")

    def test_backoff_calculation(self):
        logging.info("\n========== Starting: test_backoff_calculation ==========")

        # Test backoff calculation logic with jitter
        backoff_factor = 2
        attempt = 3
        calculated_delay = calculate_backoff(attempt, backoff_factor)

        expected_base_delay = backoff_factor * (2 ** attempt)
        # Allow for random jitter
        lower_bound = expected_base_delay - 1
        upper_bound = expected_base_delay + 1

        # Check if the calculated delay falls within the expected jitter range
        self.assertTrue(lower_bound <= calculated_delay <= upper_bound,
                        f"Calculated delay {calculated_delay} not within expected range ({lower_bound}, {upper_bound})")

        logging.info("Completed: test_backoff_calculation")

    @patch('requests.get')
    def test_exponential_backoff_integration(self, mock_get):
        logging.info("\n========== Starting: test_exponential_backoff_integration ==========")

        # Mock a transient error for the first few attempts, then success
        mock_get.side_effect = [requests.exceptions.ConnectionError] * 3 + [mock_get.return_value]
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = '<html><body>Test</body></html>'

        scraper = WebScraper(base_url="https://example.com", headers={})
        content = scraper.fetch_content(retries=3, backoff_factor=1)

        # Ensure that the content is eventually fetched
        self.assertIsNotNone(content)
        self.assertIn('Test', content)

        logging.info("Completed: test_exponential_backoff_integration")


if __name__ == '__main__':
    unittest.main()
