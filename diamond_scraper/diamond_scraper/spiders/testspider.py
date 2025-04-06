import scrapy
from scrapy_playwright.page import PageMethod
import asyncio

class MySpider(scrapy.Spider):
    name = 'test'

    def start_requests(self):
        yield scrapy.Request(
            'https://example.com',
            meta={
                "playwright": True,
                "playwright_include_page": True,
                "playwright_context": "new",
                "playwright_page_methods": [
                    PageMethod('wait_for_selector', 'body'),
                ],
            }
        )

    async def parse(self, response):
        print("arrived")
        page = response.meta.get("playwright_page")
        await asyncio.sleep(10)
        print("done")
        yield {"AAAAA": "WHY ISNT THIS WORKING"}
        if page:
            await page.close()
