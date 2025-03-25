import scrapy


class DiamondScraperItem(scrapy.Item):
    title = scrapy.Field()  # Title or name of the item being scraped
    price = scrapy.Field()  # Numeric price, ensure parsing in pipeline
    url = scrapy.Field()  # URL of the scraped page/item
    date = scrapy.Field()  # Date of the data extraction or item listing


class StockItem(scrapy.Item):
    # Basic Identifiers
    tickerSymbol = scrapy.Field()
    name = scrapy.Field()
    currency = scrapy.Field()

    # Market Data
    timestamp = scrapy.Field()
    timezone = scrapy.Field()
    price = scrapy.Field()
    priceChange = scrapy.Field()
    percentChange = scrapy.Field()

    # Trading Data
    open = scrapy.Field()
    dayLow = scrapy.Field()
    dayHigh = scrapy.Field()
    volume = scrapy.Field()
    avgVolume = scrapy.Field()

    # Company Valuation Metrics
    marketCap = scrapy.Field()
    peRatio = scrapy.Field()
    eps = scrapy.Field()


class IntoliItem(scrapy.Item):
    # General Tests
    userAgentTest = scrapy.Field()
    webDriverTest = scrapy.Field()
    webDriverAdvancedTest = scrapy.Field()
    chromeTest = scrapy.Field()
    permissionsTest = scrapy.Field()
    pluginsLengthTest = scrapy.Field()
    pluginTypeTest = scrapy.Field()
    languageTest = scrapy.Field()
    webGLVendorTest = scrapy.Field()
    webGlRendererTest = scrapy.Field()
    brokenImageDimensionsTest = scrapy.Field()

    # PhantomJS Detection
    phantom_UATest = scrapy.Field()
    phantom_PROPERTIES = scrapy.Field()
    phantom_ETSL = scrapy.Field()
    phantom_LANGUAGE = scrapy.Field()
    phantom_WEBSOCKET = scrapy.Field()
    phantom_OVERFLOW = scrapy.Field()
    phantom_WINDOW_HEIGHT = scrapy.Field()

    # Headless Chrome Detection
    headchr_UA = scrapy.Field()
    headchr_CHROME_OBJ = scrapy.Field()
    headchr_PERMISSIONS = scrapy.Field()
    headchr_PLUGINS = scrapy.Field()
    headchr_IFRAME = scrapy.Field()

    # Debugging & Tool Detection
    chr_DEBUG_TOOLS = scrapy.Field()
    selenium_DRIVER = scrapy.Field()
    sequentum = scrapy.Field()

    # Environment Data
    navigator = scrapy.Field()
    screen = scrapy.Field()
    battery = scrapy.Field()
    memory = scrapy.Field()

    # Canvas Fingerprints
    canvas1 = scrapy.Field()
    canvas2 = scrapy.Field()
    canvas3 = scrapy.Field()
    canvas4 = scrapy.Field()
    canvas5 = scrapy.Field()

    # Codec Support
    videoCodecs = scrapy.Field()
    audioCodecs = scrapy.Field()

    # Fp-collect raw dump
    fp_collect = scrapy.Field()
