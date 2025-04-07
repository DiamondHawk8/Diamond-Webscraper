import os

# ─────────────────────────────────────────────────────────────
#                      BASIC SCRAPY SETTINGS
# ─────────────────────────────────────────────────────────────

BOT_NAME = "diamond_scraper"

SPIDER_MODULES = ["diamond_scraper.spiders"]
NEWSPIDER_MODULE = "diamond_scraper.spiders"

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = "diamond_scraper (+http://www.yourdomain.com)"
# Mimic real requests
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Retry settings
RETRY_ENABLED = True
RETRY_TIMES = 2
RETRY_BACKOFF_BASE = 2

# Timeout for downloads
DOWNLOAD_TIMEOUT = 30

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# ─────────────────────────────────────────────────────────────
#                      THROTTLING / DELAYS
# ─────────────────────────────────────────────────────────────

# DOWNLOAD_DELAY = 3
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# AUTOTHROTTLE
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 5
AUTOTHROTTLE_MAX_DELAY = 60
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# AUTOTHROTTLE_DEBUG = False

# ─────────────────────────────────────────────────────────────
#                   HEADERS / COOKIES / TELNET
# ─────────────────────────────────────────────────────────────

DEFAULT_REQUEST_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en",
}

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# ─────────────────────────────────────────────────────────────
#                       SPIDER MIDDLEWARES
# ─────────────────────────────────────────────────────────────

SPIDER_MIDDLEWARES = {
    # Session stats only executes on close, so order doesn't affect it much
    "diamond_scraper.middlewares.core_middlewares.SessionStatsLoggerMiddleware": 100,
    "diamond_scraper.middlewares.core_middlewares.DiamondScraperSpiderMiddleware": 543,
}

# ─────────────────────────────────────────────────────────────
#                     DOWNLOADER MIDDLEWARES
# ─────────────────────────────────────────────────────────────

DOWNLOADER_MIDDLEWARES = {
    "diamond_scraper.middlewares.core_middlewares.DiamondScraperDownloaderMiddleware": 543,
    "diamond_scraper.middlewares.proxy_rotation_middleware.ProxyRotationMiddleware": 543,
}

# ─────────────────────────────────────────────────────────────
#                     PLAYWRIGHT HANDLER
# ─────────────────────────────────────────────────────────────

DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}

# ─────────────────────────────────────────────────────────────
#                         PIPELINES
# ─────────────────────────────────────────────────────────────

ITEM_PIPELINES = {
    # "diamond_scraper.pipelines.core_pipelines.DiamondScraperPipeline": 100,
    # "diamond_scraper.pipelines.InvalidDataPipeline": 200,
    "diamond_scraper.pipelines.core_pipelines.DuplicatesPipeline": 300,
    "diamond_scraper.pipelines.db_pipeline.DatabasePipeline": 998,
    # "diamond_scraper.pipelines.TestPipeline": 999,
}

# ─────────────────────────────────────────────────────────────
#                 FEEDS / DATA EXPORT FORMATS
# ─────────────────────────────────────────────────────────────

FEEDS = {
    "data.jl": {
        "format": "jsonlines",
        "encoding": "utf8",
        "indent": 4,
    }
}

# ─────────────────────────────────────────────────────────────
#                     HTTP CACHE (DISABLED)
# ─────────────────────────────────────────────────────────────

HTTPCACHE_ENABLED = False
HTTPCACHE_EXPIRATION_SECS = 3600
HTTPCACHE_DIR = "httpcache"
HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# ─────────────────────────────────────────────────────────────
#              PLAYWRIGHT & TWISTED ASYNC REACTOR
# ─────────────────────────────────────────────────────────────

TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

LOG_DIR = os.path.join(os.getcwd(), "logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "scrapy_output.log")
LOG_LEVEL = "INFO"


LOG_FILE_APPEND = False

# ─────────────────────────────────────────────────────────────
#                  PLAYWRIGHT CONFIGURATION
# ─────────────────────────────────────────────────────────────

PLAYWRIGHT_BROWSER_TYPE = "chromium"  # can also use firefox or webkit
PLAYWRIGHT_LAUNCH_OPTIONS = {
    "headless": False,
    "timeout": 30 * 1000,
    "devtools": True,
    "slow_mo": 500,
}
PLAYWRIGHT_DEFAULT_CONTEXT_OPTIONS = {
    "viewport": None,  # allows native window sizing
    "ignoreHTTPSErrors": True,
}
PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT = 20 * 1000
PLAYWRIGHT_MAX_CONTEXTS = 1

# ─────────────────────────────────────────────────────────────
#                     PROXY / STEALTH SETTINGS
# ─────────────────────────────────────────────────────────────
"""
PROXY_LIST = [
    "http://51.158.68.133:8811",
    "http://64.225.8.82:9981",
    "http://185.199.228.146:7492",
    "http://138.68.60.8:8080",
    "http://20.94.229.49:3128",
]
"""
# PROXY_LIST = os.getenv("PROXY_LIST", "").split(",")
FALLBACK_PROXY = None

