import os
import sys
import argparse
import datetime
from pathlib import Path
from scrapy.cmdline import execute


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
                        help='Specify the logging level, overwrites any LOG_LEVEL provided in --settings')

    # Output config
    parser.add_argument('-o', '--output', type=str, help='Output file')
    parser.add_argument('-O', '--overwrite-output', action='store_true', help='Overwrite output file')
    parser.add_argument('-f', '--output-format', type=str,
                        choices=['json', 'jsonlines', 'csv', 'xml'],
                        help='Output format (requires --output)')

    # Behavior modifiers
    parser.add_argument('-n', '--no-cache', action='store_true', help='Disable caching')
    parser.add_argument('-j', '--job-dir', type=str, help='Persistent job dir for pausing/resuming, '
                                                          'overwrites --settings')
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


def run_spider(spider_name: str, args, env_settings: dict):
    """
    Assemble and execute the Scrapy command for a given spider.

    Responsibilities:
    1. Build the base Scrapy CLI command.
    2. Add output destination and format.
    3. Inject Scrapy settings from both CLI and setup_environment().
    4. Respect CLI flags like --job-dir, --no-cache, and --dry-run.
    5. Execute or print the command based on --dry-run.

    Parameters:
    - spider_name: str — The name of the spider to run
    - args: argparse.Namespace — Parsed CLI arguments from user input
    - env_settings: dict — Derived environment settings (e.g., LOG_FILE) from setup_environment()
    """

    command = ['scrapy', 'crawl', spider_name]

    #  Output file logic 
    if args.output:
        command.extend(['-o', args.output])

    if args.overwrite_output:
        command.extend(['-O'])

    if args.output_format:
        command.extend(['-t', args.output_format])

    #  Inject jobdir (if not overridden by --settings) 
    if args.job_dir is not None:
        command.extend(['-s', f'JOBDIR={args.job_dir}'])

    # Inject environment-derived settings (e.g., log path, tags)
    for key, value in env_settings.items():
        command.extend(['-s', f'{key}={value}'])

    #  Inject settings from --settings unless overridden
    for setting in (args.settings or []):
        # Respect CLI overrides for JOBDIR and LOG_LEVEL
        if setting.upper().startswith('JOBDIR=') and args.job_dir is not None:
            continue
        if setting.upper().startswith('LOG_LEVEL=') and args.log_level is not None:
            continue
        command.extend(['-s', setting])

    #  Inject log level if not already overridden 
    if not any(s.upper().startswith('LOG_LEVEL=') for s in (args.settings or [])):
        command.extend(['-s', f'LOG_LEVEL={args.log_level}'])

    #  Disable caching if requested 
    if args.no_cache:
        command.extend(['-s', 'HTTPCACHE_ENABLED=False'])

    #  Dry-run mode: print command and skip execution 
    if args.dry_run:
        print("Dry run command:", " ".join(command))
        return

    execute(command)


def main():
    """
    1. Parse arguments
    2. Set up the runtime environment
    3. Call run_spider() with the appropriate name and options
    """
    args = parse_arguments()
    env_settings = setup_environment(args)

    for spider_name in args.spiders:
        run_spider(spider_name, args, env_settings)


if __name__ == "__main__":
    main()
