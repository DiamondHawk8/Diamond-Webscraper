import os
import sys
import argparse
import datetime
from pathlib import Path

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
    parser.add_argument('-lf', '--log-file', type=str, help='Custom log file name')
    parser.add_argument('-l', '--log-level', type=str, default='INFO',
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                        help='Specify the logging level')

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


def setup_environment(args):
    """
    Optionally configure environment variables, logging paths, or settings overrides here.
    """

    env_settings = {}

    # Ensure path is added to module search path at runtime
    abs_path = os.path.dirname(os.path.abspath(__file__))
    if abs_path not in sys.path:
        sys.path.append(abs_path)

    # If user provides --log-file, use it.
    # Otherwise, construct a default one using datetime format (e.g. logs/scraper_YYYYMMDD_HHMMSS.log)
    if args.log_file is not None:
        Path(args.log_file).parent.mkdir(parents=True, exist_ok=True)
        env_settings['LOG_FILE'] = args.log_file
    else:
        time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        Path(f"logs/scraper_{time}").parent.mkdir(parents=True, exist_ok=True)
        env_settings['LOG_FILE'] = f"logs/scraper_{time}.log"

    # Update the log file path
    if args.tags is not None:
        env_settings['TAGS'] = args.tags

    return env_settings


def run_spider(spider_name: str, args, env_settings):

    #
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
    setup_environment(parsed_args)

    for spider_name in parsed_args.spiders:
        run_spider(spider_name, parsed_args)
    pass


if __name__ == "__main__":
    main()
