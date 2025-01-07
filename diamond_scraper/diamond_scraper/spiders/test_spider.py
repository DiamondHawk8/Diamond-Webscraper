from pathlib import Path

import scrapy
from scrapy import Request


class TestSpider(scrapy.Spider):
    # identifies the spider
    name = "test"
    # automatically passed to parse, since its scrapys default

    start_urls = [
        "https://quotes.toscrape.com/page/1/",
        "https://quotes.toscrape.com/page/2/",
    ]


    
    """
    # Returns an iterable of Requests that the spider will crawl, also not necessary
    def start_requests(self):
        urls = [
            "https://quotes.toscrape.com/page/1/",
            "https://quotes.toscrape.com/page/2/",
        ]
        # for every url, scrapy creates a request with the parse method as a callback
        for url in urls:
            yield Request(url=url, callback=self.parse)
    """

    # method for parsing responses, finding new urls and creating new requests from them
    def parse(self, response, **kwargs):
        for quote in response.css("div.quote"):
            yield {
                "text": quote.css('span.text::text').get(),
                "author": quote.css('small.author::text').get(),
                "tags": quote.css('div.tags a.tag::text').getall(),
            }
        next_page = response.css("li.next a::attr(href)").get()
        # This could also be used, since .follow will automatically pull the necessary attributes from a selector
        # next_page = response.css("li.next a::attr(href)")

        # You could shorten it even further by using:
        """
        for a in response.css("ul.pager a"):
            yield response.follow(a, callback=self.parse)
        """
        # As .follow will automatically extract href

        if next_page:
            # You can manually join the link using urljoin (which automatically figures out how to attach it)
            """
            next_page = response.urljoin(next_page)
            yield Request(url=next_page, callback=self.parse)
            """
            # You can also just use response.follow
            yield response.follow(next_page, callback=self.parse)

        """
        Assuming multiple links, we can use response.follow_all
        anchors = response.css("ul.pager a")
        yield from response.follow_all(anchors, callback=self.parse)
        
        this does the same as the two lines above
        yield from response.follow_all(css="ul.pager a", callback=self.parse)
        """
