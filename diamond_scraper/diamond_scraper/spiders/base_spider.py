import scrapy
from scrapy.crawler import CrawlerProcess


class BaseSpider(scrapy.Spider):
    name = 'base'
    urls = ["https://www.marketwatch.com/investing/stock/tsla"]
    custom_settings = {
        "FEED_FORMAT": "json",
        "FEED_URI": "output.json",
    }
    # var to track total price of books
    total_price = 0
    books_scraped = 0
    max_depth = 3

    def start_requests(self):
        for url in self.urls:
            # yield scrapy.Request(url=url, callback=self.parse)
            yield scrapy.Request(url=url, callback=self.parse_market_watch)


    def parse_market_watch(self, response):
        # Basic Identifiers
        tickerSymbol = response.css("span.company__ticker::text").get()
        name = response.css("h1.company__name::text").get()
        currency = response.css("h2.intraday__price sup.character::text").get()

        # Market Data
        timestamp = response.css("span.timestamp__time bg-quote::text").get()
        timezone = response.css("span.timestamp__time::text").getall()[-1]
        price = response.css("h2.intraday__price bg-quote::text").get()
        priceChange = response.css("h2.intraday__price sup.character::text").get()
        percentChange = response.css("h2.intraday__price bg-quote::text").get()

        # Trading Data
        volume = response.css("div.range__header span.primary::text").get()
        table_items = response.css("div.region.region--primary ul.list.list--kv.list--col50 li.kv__item "
                                   "span.primary::text").getall()
        open = table_items[0]
        dayLow = table_items[1][:table_items[1].index("-")]
        dayHigh = table_items[1][table_items[1].index("-") + 1:]
        avgVolume = table_items[15]

        # Company Valuation Metrics
        marketCap = table_items[3]
        peRatio = table_items[8]
        eps = table_items[9]

        yield {
            "tickerSymbol": tickerSymbol,
            "name": name,
            "currency": currency,
            "timestamp": timestamp,
            "timezone": timezone,
            "price": price,
            "priceChange": priceChange,
            "percentChange": percentChange,
            "open": open,
            "dayLow": dayLow,
            "dayHigh": dayHigh,
            "volume": volume,
            "avgVolume": avgVolume,
            "marketCap": marketCap,
            "peRatio": peRatio,
            "eps": eps,
        }


