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

