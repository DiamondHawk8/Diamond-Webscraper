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
    pluginsTypeTest = scrapy.Field()
    languageTest = scrapy.Field()
    webGLVendorTest = scrapy.Field()
    webGLRendererTest = scrapy.Field()
    brokenImageDimensionsTest = scrapy.Field()

    # PhantomJS Detection
    phantomUaTest = scrapy.Field()
    phantomPropertiesTest = scrapy.Field()
    phantomEtslTest = scrapy.Field()
    phantomLanguageTest = scrapy.Field()
    phantomWebsocketTest = scrapy.Field()
    phantomOverflowTest = scrapy.Field()
    phantomWindowHeightTest = scrapy.Field()

    # Headless Chrome Detection
    headchrUaTest = scrapy.Field()
    headchrChromeObjTest = scrapy.Field()
    headchrPermissionsTest = scrapy.Field()
    headchrPluginsTest = scrapy.Field()
    headchrIframeTest = scrapy.Field()

    # Debugging & Tool Detection
    chromeDebugToolsTest = scrapy.Field()
    seleniumDriverTest = scrapy.Field()
    sequentumTest = scrapy.Field()

    # Environment Data
    navigatorTest = scrapy.Field()
    screenTest = scrapy.Field()
    batteryTest = scrapy.Field()
    memoryTest = scrapy.Field()

    # Canvas Fingerprints
    canvas1Test = scrapy.Field()
    canvas2Test = scrapy.Field()
    canvas3Test = scrapy.Field()
    canvas4Test = scrapy.Field()
    canvas5Test = scrapy.Field()

    # Codec Support
    videoCodecsTest = scrapy.Field()
    audioCodecsTest = scrapy.Field()

    # Full raw dump (if needed for fallback or debugging)
    fpCollectDump = scrapy.Field()
