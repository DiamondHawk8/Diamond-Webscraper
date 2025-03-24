import os
import sys
import argparse

# Ensure path is added to module search path at runtime
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def parse_arguments():
    """
    Parse command-line arguments to determine which spider(s) to run and how to configure the Scrapy runtime.

    Supports:
    - Multiple spider names
    - Logging control
    - Output destination and format
    - Dynamic Scrapy settings via `-s`
    - Optional tag metadata
    - Dry-run mode
    """

    parser = argparse.ArgumentParser(description='Diamond Webscraper Runner')

    # Required positional arg: one or more spiders
    parser.add_argument('spiders', nargs='+', help='Spiders to run')

    # Optional settings overrides
    parser.add_argument('-s', '--settings', nargs='+', help='Override Scrapy settings (e.g. -s LOG_LEVEL=DEBUG)')

    # Logging control
    parser.add_argument('-l', '--log-level', type=str, default='INFO',
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                        help='Specify the logging level')
    parser.add_argument('-lf', '--log-file', type=str, help='Custom log file name')

    # Output config
    parser.add_argument('-o', '--output', type=str, help='Output file')
    parser.add_argument('-f', '--output-format', type=str,
                        choices=['json', 'jsonlines', 'csv', 'xml'],
                        help='Output format (requires --output)')

    # Behavior modifiers
    parser.add_argument('-n', '--no-cache', action='store_true', help='Disable caching')
    parser.add_argument('-j', '--job-dir', type=str, help='Persistent job dir for pausing/resuming')
    parser.add_argument('-t', '--tags', nargs='+', help='Optional tags for labeling the run')
    parser.add_argument('-d', '--dry-run', action='store_true', help='Print command but do not execute it')

    return parser.parse_args()


def setup_environment():
    """
    Optionally configure environment variables, logging paths, or settings overrides here.
    TODO:
    - Dynamically set LOG_FILE path using today's date
    - Add project directory to sys.path
    - Export Scrapy environment settings if needed
    """
    pass


def run_spider(spider_name: str, args):
    """
    Execute the given spider using Scrapy’s command-line interface from within Python.

    Arguments:
    - spider_name: str – name of the spider to run (must match Scrapy's spider name)
    - extra_args: list – optional additional arguments (maybe log level, output file, more?)

    Potential Uses:
    - scrapy.cmdline.execute([...])
    """
    pass


def main():
    """
    1. Parse arguments
    2. Set up the runtime environment
    3. Call run_spider() with the appropriate name and options
    """
    parsed_args = parse_arguments()
    setup_environment()

    for spider_name in parsed_args.spiders:
        run_spider(spider_name, parsed_args)
    pass


if __name__ == "__main__":
    main()
