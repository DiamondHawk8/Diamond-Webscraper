import scrapy


class BaseSpider(scrapy.Spider):
    name = 'base_spider'
    urls = ["https://quotes.toscrape.com/"]
    custom_settings = {} # Uncertain of what setting will be needed

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse)

    # Using https://quotes.toscrape.com/ for now
    def parse(self, response, **kwargs):
        pass

