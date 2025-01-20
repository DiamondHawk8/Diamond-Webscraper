import scrapy


class DiamondScraperItem(scrapy.Item):
    title = scrapy.Field()  # Title or name of the item being scraped
    price = scrapy.Field()  # Numeric price, ensure parsing in pipeline
    url = scrapy.Field()  # URL of the scraped page/item
    date = scrapy.Field()  # Date of the data extraction or item listing


# TODO: Add different items for different scraping items
