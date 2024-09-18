import requests
import logging
import time


class WebScraper:
    """
    A class to fetch and parse data from websites.
    """

    def __init__(self, base_url, headers, timeout=10):
        """
        Initializes the WebScraper instance.

        Args:
            base_url (str): The base URL for scraping.
            headers (dict): HTTP headers for the requests.

        """
        self.base_url = base_url
        self.headers = headers

        self.fetch_content(self.base_url, timeout=timeout)
        pass  # Replace with initialization logic

    # TODO Implement retries and delay and timeout from config.yaml
    def fetch_content(self, url=None, retries=3, delay=2, timeout=5):
        """
        Fetches HTML content from the specified URL.

        Args:
            url (str): The URL of the webpage to fetch. Defaults to base_url if not provided.

        Returns:
            str: The HTML content of the page.

        Error Handling:
            - Catch network exceptions (e.g., timeouts, connection errors).
            - Handle HTTP errors (e.g., 4xx, 5xx status codes).
            - Log errors for debugging purposes.
        """

        if url is None:
            url = self.base_url
        tries = 0
        logging.info("Starting to fetch page {}".format(url))
        while tries < retries:
            try:
                r = requests.get(url, timeout=timeout)
                r.raise_for_status()  # raise error
                print(f"Successfully fetched page on attempt {tries + 1}")
                logging.info(f"Successfully fetched page on attempt {tries + 1}")
                return r
            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
                tries += 1
                logging.warning(f"Failed to fetch page on attempt {tries}, retrying in {delay} seconds")
                time.sleep(delay)
            except requests.exceptions.HTTPError as e:
                logging.error(f"HTTP error occurred: {e}")
                return None
        logging.error(f"Failed to fetch page after {tries} attempts for {url}")
        return None

    def parse_content(self, html_content):
        """
        Parses HTML content and extracts relevant data.

        Args:
            html_content (str): The HTML content to parse.

        Returns:
            list: A list of dictionaries containing extracted data.

        Error Handling:
            - Handle parsing errors (e.g., AttributeError if elements are not found).
            - Ensure valid data is extracted (e.g., check if elements exist).

        Suggested Implementation Steps:
            - Use `BeautifulSoup` to parse the HTML content.
            - Locate relevant elements using CSS selectors or tags.
            - Store the extracted data in a structured format (list of dicts).
        """
        # Step 1: Create a BeautifulSoup object from the HTML content.
        # Step 2: Use CSS selectors or tags to locate data.
        # Step 3: Store the extracted data in a structured format (list, dictionary, etc.).

        pass  # Replace with parsing logic
