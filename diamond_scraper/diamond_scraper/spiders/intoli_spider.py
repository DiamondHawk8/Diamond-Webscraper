import scrapy

class IntoliSpider(scrapy.Spider):
    name = 'IntoliSpider'
    urls = ["https://bot.sannysoft.com/"]
    def start_requests(self):
        for url in self.urls:
            self.logger.info(f"Beginning request for url: {url}")
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        pass


