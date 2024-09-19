import requests
import logging
import time
from bs4 import BeautifulSoup


class WebScraper:
    """
    A class to fetch and parse data from websites
    """

    def __init__(self, base_url, headers, timeout=10):
        self.base_url = base_url
        self.headers = headers
        self.content = self.fetch_content(self.base_url, timeout=timeout)
        self.parsed_content = self.parse_content(self.content)

    def fetch_content(self, url=None, retries=3, delay=2, timeout=5):
        """
        Fetches HTML content from the specified URL.

        Args:
            url (str): The URL to fetch content from. If None, uses self.base_url.
            retries (int): Number of retry attempts on failure. Defaults to 3.
            delay (int): Delay in seconds between retries. Defaults to 2 seconds.
            timeout (int): Timeout in seconds for the HTTP request. Defaults to 5 seconds.

        Returns:
            str: The HTML content of the page, or None if all retries fail.

        """

        if url is None:
            url = self.base_url

        tries = 0
        logging.info(f"Starting to fetch page: {url}")

        while tries < retries:
            try:
                response = requests.get(url, headers=self.headers, timeout=timeout)
                response.raise_for_status()  # Raise HTTPError for bad responses
                logging.info(f"Successfully fetched page on attempt {tries + 1}")
                return response.text
            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
                tries += 1
                logging.warning(f"Attempt {tries} failed: {e}. Retrying in {delay} seconds.")
                time.sleep(delay)
            except (requests.exceptions.HTTPError, requests.exceptions.RequestException) as e:
                logging.error(f"HTTP error occurred: {e}")
                return None

        logging.error(f"Failed to fetch page after {tries} attempts for {url}")
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
