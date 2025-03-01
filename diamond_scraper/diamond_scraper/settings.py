# Scrapy settings for diamond_scraper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

# TODO, configure more advanced default settings

BOT_NAME = "diamond_scraper"

SPIDER_MODULES = ["diamond_scraper.spiders"]
NEWSPIDER_MODULE = "diamond_scraper.spiders"

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "diamond_scraper (+http://www.yourdomain.com)"

# Mimic real requests
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

RETRY_ENABLED = True
# 2 retries for a total of 3 attempts
RETRY_TIMES = 2
# Exponential backoff starting at 2 seconds
RETRY_BACKOFF_BASE = 2
DOWNLOAD_TIMEOUT = 30

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en",
}


SPIDER_MIDDLEWARES = {
    # Session stats only executes on close, so order doesn't affect it much
    "diamond_scraper.middlewares.SessionStatsLoggerMiddleware": 100,
    "diamond_scraper.middlewares.DiamondScraperSpiderMiddleware": 543,
}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    "diamond_scraper.middlewares.DiamondScraperDownloaderMiddleware": 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

ITEM_PIPELINES = {
    "diamond_scraper.pipelines.DiamondScraperPipeline": 100,
    "diamond_scraper.pipelines.InvalidDataPipeline": 200,
    "diamond_scraper.pipelines.DuplicatesPipeline": 300,
}

FEEDS = {
    'data.jl': {
        'format': 'jsonlines',
        'encoding': 'utf8',
        'indent': 4,
    }
}

AUTOTHROTTLE_ENABLED = True

# Base delay time
AUTOTHROTTLE_START_DELAY = 5

# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# TODO turn off after development is done
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 3600
HTTPCACHE_DIR = "httpcache"
HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

LOG_FILE = "scraper.log"
LOG_LEVEL = "INFO"

