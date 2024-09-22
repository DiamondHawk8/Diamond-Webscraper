import requests
import logging
import time
from bs4 import BeautifulSoup
import random


def calculate_backoff(attempt, backoff_factor):
    """
    Calculates the backoff factor to prevent detection of automated retries
    :returns delay (int): The delay in seconds to wait between retries.
    """
    delay = backoff_factor * (2 ** attempt)
    jitter = random.uniform(0, 1)  # Adds random jitter between 0 and 1 second.
    return delay + jitter


class WebScraper:
    """
    A class to fetch and parse data from websites
    """

    def __init__(self, base_url, headers, timeout=10):
        self.base_url = base_url
        self.headers = headers
        self.timeout = timeout

    def fetch_content(self, url=None, max_retries=3, backoff_factor=2):
        """
        Fetches HTML content from the specified URL with retry logic.

        Args:
            url (str): The URL to fetch content from.
            max_retries (int): Maximum number of retry attempts.
            backoff_factor (int): Factor for calculating backoff time.

        Returns:
            str: HTML content if successful, None otherwise.
        """
        if url is None:
            url = self.base_url

        attempt = 0
        logging.info(f"Starting to fetch page: {url}")

        while attempt < max_retries:
            try:
                response = requests.get(url, headers=self.headers, timeout=self.timeout)
                response.raise_for_status()
                logging.info(f"Successfully fetched page on attempt {attempt + 1}")
                return response.text
            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
                delay = calculate_backoff(attempt, backoff_factor)
                logging.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay:.2f} seconds.")
                time.sleep(delay)
                attempt += 1
            except requests.exceptions.HTTPError as e:
                status_code = e.response.status_code
                if 500 <= status_code < 600:
                    # Server error, retry
                    delay = calculate_backoff(attempt, backoff_factor)
                    logging.warning(
                        f"Server error {status_code} on attempt {attempt + 1}: {e}. Retrying in {delay:.2f} seconds.")
                    time.sleep(delay)
                    attempt += 1
                else:
                    # Client error, do not retry
                    logging.error(f"Client error {status_code}: {e}")
                    return None
            except requests.exceptions.RequestException as e:
                logging.error(f"Request exception occurred: {e}")
                return None

        logging.error(f"Failed to fetch page after {max_retries} attempts for {url}")
        return None

    def parse_content(self, html_content):
        """
        Parses the HTML content and extracts relevant data (e.g., links).

        Args:
            html_content (str): The HTML content to parse.

        Returns:
            list: A list of unique URLs extracted from the page.

        """
        if not html_content:
            logging.error("No HTML content to parse.")
            return []

        soup = BeautifulSoup(html_content, 'html.parser')
        tags = soup.find_all("a")
        content = []
        for tag in tags:
            val = tag.get('href')
            if val and val not in content:  # Ensure uniqueness
                content.append(val)

        logging.info(f"Extracted {len(content)} unique URLs from the page.")
        return content
