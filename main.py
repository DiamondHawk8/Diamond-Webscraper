from scraper import WebScraper
from utils import load_config
from data_processor import DataProcessor
import logging
import os


def main():
    """
    Main function to run the web scraping and data processing workflow.
    """

    # Load configuration from config.yaml
    config = load_config()
    logging.info("Config loaded")

    # Check to see if the URL actually exists
    if 'base_url' not in config:
        logging.error("Missing 'base_url' in configuration. Exiting.")
        return

    scraper = WebScraper(
        base_url=config['base_url'],
        headers=config['headers'],
        timeout=config.get('timeout', 10)
    )

    html_content = scraper.fetch_content(
        retries=config.get('retries', 3), delay=config.get('delay', 2), timeout=config.get('timeout', 10))

    if not html_content:
        # Logging already handled in scraper.py
        # logging.error(f"Failed to fetch content from {scraper.base_url}")
        print("Error: Failed to fetch content.")
        return

    logging.info("HTML content loaded")

    # Parse the fetched content
    parsed_data = scraper.parse_content(html_content)
    logging.info("Parsed HTML content")
    print(f"Extracted {len(parsed_data)} items.")

    if not parsed_data:
        logging.warning("No data parsed from HTML content.")
        return

    # Process data
    processor = DataProcessor(parsed_data)

    save_path = config.get('save_location', 'data.csv')
    save_dir = os.path.dirname(save_path)

    # Se if the directory exists
    if save_dir and not os.path.exists(save_dir):
        os.makedirs(save_dir)

    processor.save_data(save_path, config.get('format', 'csv'))
    print(f"Saved {len(parsed_data)} items.")
    logging.info("Data saved")


if __name__ == '__main__':
    main()
