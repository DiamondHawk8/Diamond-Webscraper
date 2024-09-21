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
        self.content = self.fetch_content(self.base_url, timeout=timeout)
        self.parsed_content = self.parse_content(self.content)

    def fetch_content(self, url=None, retries=3, backoff_factor=2, timeout=10):
        """
        Fetches HTML content from the specified URL.
        """

        if url is None:
            url = self.base_url

        attempt = 0
        logging.info(f"Starting to fetch page: {url}")

        # Loop to handle retries
        while attempt < retries:
            delay = calculate_backoff(attempt, backoff_factor)

            # Attempt to get response from url
            try:
                response = requests.get(url, headers=self.headers, timeout=timeout)
                response.raise_for_status()  # Raise HTTPError for bad responses
                logging.info(f"Successfully fetched page on attempt {attempt + 1}")
                return response.text

            # Except non fatal errors
            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
                attempt += 1
                logging.warning(f"Attempt {attempt} to fetch {url} failed: {e}. Retrying in {delay:.2f} seconds.")
                time.sleep(delay)

            except (requests.exceptions.HTTPError, requests.exceptions.RequestException) as e:
                logging.error(f"HTTP error occurred: {e}")
                return None

        logging.error(f"Failed to fetch page after {attempt} attempts for {url}")
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

