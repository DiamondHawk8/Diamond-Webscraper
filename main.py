from scraper import WebScraper
from utils import load_config
from data_processor import DataProcessor
import logging


def main():
    """
    Main function to run the web scraping and data processing workflow.
    """

    # Load configuration from config.yaml
    config = load_config()
    logging.info("Config loaded")

    scraper = WebScraper(
        base_url=config['base_url'],
        headers=config['headers'],
        timeout=config.get('timeout', 10)
    )

    html_content = scraper.fetch_content(
        retries=config.get('retries', 3), delay=config.get('delay', 2), timeout=config.get('timeout', 10))
    logging.info("HTML content loaded")

    parsed_data = []
    # Parse the fetched content if successful
    if html_content:
        parsed_data = scraper.parse_content(html_content)
        logging.info("Parsed HTML content")
        print(f"Extracted {len(parsed_data)} items.")
    else:
        logging.warning("HTML content not loaded")
        print("Failed to fetch content.")

    # Process data
    if parsed_data:
        processor = DataProcessor(parsed_data)
        processor.clean_data()
        processor.save_data(config.get('save_data', 'data.csv'), config.get('format', 'csv'))
        print(f"Saved {len(parsed_data)} items.")
        logging.info("Data saved")


if __name__ == '__main__':
    main()

