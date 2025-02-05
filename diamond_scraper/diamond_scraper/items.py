import scrapy


class DiamondScraperItem(scrapy.Item):
    title = scrapy.Field()  # Title or name of the item being scraped
    price = scrapy.Field()  # Numeric price, ensure parsing in pipeline
    url = scrapy.Field()  # URL of the scraped page/item
    date = scrapy.Field()  # Date of the data extraction or item listing


class YahooFinanceStockItem(scrapy.Item):
    tickerSymbol = scrapy.Field()
    name = scrapy.Field()
    currency = scrapy.Field()

    # Regular fields
    timestamp = scrapy.Field()
    price = scrapy.Field()
    priceChange = scrapy.Field()
    percentChange = scrapy.Field()

    # After hours fields
    AHtimestamp = scrapy.Field()
    AHprice = scrapy.Field()
    AHpriceChange = scrapy.Field()
    AHpercentChange = scrapy.Field()
