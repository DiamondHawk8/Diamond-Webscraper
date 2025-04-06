import scrapy
from scrapy_playwright.page import PageMethod
import time

class MySpider(scrapy.Spider):
    name = 'test'

    def start_requests(self):
        yield scrapy.Request(
            'https://example.com',
            meta=dict(
                playwright=True,
                playwright_include_page=True,
                playwright_page_methods=[
                    PageMethod('wait_for_selector', 'body'),
                ]
            )
        )

    def parse(self, response):
        time.sleep(2)
        return {"AAAAA":"WHY ISNT THIS WORKING"}