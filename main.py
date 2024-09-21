import utils
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

    utils.setup_logging(log_file=config.get('log_file', 'scraper.log'), log_level=config.get('log_level', 'INFO'))

    logging.info("Config loaded")

    scraper = WebScraper(
        base_url=config['base_url'],
        headers=config['headers'],
        timeout=config.get('timeout', 10)
    )

    html_content = scraper.fetch_content(
        retries=config.get('retries', 3),
        backoff_factor=config.get('backoff_factor', 2),
        timeout=config.get('timeout', 10)
    )
    logging.info("HTML content loaded")

    parsed_data = []
    if html_content:
        parsed_data = scraper.parse_content(html_content)
        logging.info(f"Parsed {len(parsed_data)} items from HTML content")

    if parsed_data:
        processor = DataProcessor(parsed_data)
        processor.clean_data()
        processor.save_data(config.get('save_data', 'data.csv'), config.get('format', 'csv'))
        logging.info(f"Saved {len(parsed_data)} items to file.")

    # End of scraping session
    logging.info("========== End of scraping session ==========")


if __name__ == '__main__':
    main()