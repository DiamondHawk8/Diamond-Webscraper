import utils
from scraper import WebScraper
from utils import load_config
from data_processor import DataProcessor
import logging
import os


def main():
    # Load configuration from config.yaml
    config = load_config()

    # Access logging settings
    log_file = config['logging'].get('log_file', 'scraper.log')
    log_level = config['logging'].get('log_level', 'INFO')
    utils.setup_logging(log_file=log_file, log_level=log_level)

    logging.info("Config loaded")

    scraper = WebScraper(
        base_url=config['base_url'],
        headers=config['headers'],
        timeout=config.get('timeout', 10)
    )

    html_content = scraper.fetch_content(
        max_retries=config['retry'].get('max_retries', 3),
        backoff_factor=config['retry'].get('backoff_factor', 2)
    )
    logging.info("HTML content loaded")

    parsed_data = []
    if html_content:
        parsed_data = scraper.parse_content(html_content)
        logging.info(f"Parsed {len(parsed_data)} items from HTML content")

    if parsed_data:
        processor = DataProcessor(parsed_data)

        logging.info("Cleaning data...")

        data_frame = processor.clean_data()

        if config.get('missing_data_strategy') == 'fill_value':
            data_frame = processor.handle_missing_data(
                data_frame=data_frame,
                strategy='fill_value',
                value=config.get('value', 0),
            )
        else:
            data_frame = processor.handle_missing_data(
                data_frame=data_frame,
                strategy=config.get('missing_data_strategy', 'fill_mean'),
            )

        logging.info(f"Missing data handled using strategy: {config.get('missing_data_strategy')}")
        logging.info(f"Dataframe finished cleaning with {len(data_frame)} rows remaining")

        processor.save_data(
            data_frame,
            config['data_saving'].get('save_location', 'data.csv'),
            config['data_saving'].get('file_format', 'csv')
        )
        logging.info(f"Saved {len(parsed_data)} items to file.")

        # Data Visualization
        visualization_types = config['visualization'].get('types', ['histogram', 'bar_chart'])
        output_dir = config['visualization'].get('output_dir', 'visualizations/')

        logging.info("Generating data visualizations...")
        processor.visualize_data(data_frame, output_dir, visualization_types)
        logging.info("Data visualizations completed.")

        # End of scraping session
        logging.info("========== End of scraping session ==========")


if __name__ == '__main__':
    main()
