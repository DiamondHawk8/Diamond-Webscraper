import unittest
from scraper import WebScraper
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

        mock_get.return_value.status_code = 200
        mock_get.return_value.text = '<html><body>Test</body></html>'

        scraper = WebScraper(base_url="https://example.com", headers={})
        content = scraper.fetch_content()

        self.assertIsNotNone(content)
        self.assertIn('Test', content)

        logging.info("Completed: test_fetch_content_success")

    @patch('requests.get')
    def test_fetch_content_failure(self, mock_get):
        logging.info("\n========== Starting: test_fetch_content_failure ==========")

        mock_get.side_effect = requests.exceptions.RequestException

        scraper = WebScraper(base_url="https://example.com", headers={})
        content = scraper.fetch_content()

        self.assertIsNone(content)

        logging.info("Completed: test_fetch_content_failure")

    def test_parse_content(self):
        logging.info("\n========== Starting: test_parse_content ==========")

        html_content = '<html><body><a href="https://link1.com">Link1</a></body></html>'
        scraper = WebScraper(base_url="https://example.com", headers={})
        parsed_data = scraper.parse_content(html_content)

        self.assertIn('https://link1.com', parsed_data)

        logging.info("Completed: test_parse_content")


if __name__ == '__main__':
    unittest.main()
