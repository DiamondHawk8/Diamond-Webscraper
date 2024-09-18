from scraper import WebScraper
from utils import load_config


def main():
    """
    Main function to run the web scraping and data processing workflow.
    """

    # Load configuration from config.yaml
    config = load_config()

    scraper = WebScraper(
        base_url=config['base_url'],
        headers=config['headers'],
        timeout=config.get('timeout', 10)
    )

    html_content = scraper.fetch_content(
        retries=config.get('retries', 3), delay=config.get('delay', 2), timeout=config.get('timeout', 10))

    # Parse the fetched content if successful
    if html_content:
        parsed_data = scraper.parse_content(html_content)
        print(f"Extracted {len(parsed_data)} items.")
    else:
        print("Failed to fetch content.")


if __name__ == '__main__':
    main()
