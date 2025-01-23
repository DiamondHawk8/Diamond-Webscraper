import scrapy
from scrapy.crawler import CrawlerProcess


class BaseSpider(scrapy.Spider):
    name = 'base'
    urls = ["https://en.wikipedia.org/wiki/World_War_II"]
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
            yield scrapy.Request(url=url, callback=self.parse_wikipedia)

    # Extract all categories of a given wikipedia page, and follow any see also links to a give depth
    def parse_wikipedia(self, response):
        # Get the depth of the request, with 0 as default to account for first request
        current_depth = response.meta.get('depth', 0)
        title = response.css("span.mw-page-title-main::text").get()
        categories = response.css("div.mw-normal-catlinks ul li a::attr(href)").getall()
        cleaned_categories = []

        for category in categories:
            category = category.strip()[category.index(":")+1:].replace('_', " ")
            cleaned_categories.append(category)
        if current_depth < self.max_depth:
            follow_links = response.css("div.mw-heading.mw-heading2 + ul li a::attr(href)").getall()
            if len(follow_links) > 0:
                for link in follow_links:
                    if "/wiki/" in link:
                        yield response.follow(link, callback=self.parse_wikipedia,
                                              meta={"depth": current_depth + 1})


        yield {'title': title,
               'categories': cleaned_categories,
               'depth': current_depth
               }



    def parse_books(self, response):
        # For each book container in site
        for book in response.css('article.product_pod'):
            # Extract the book page link
            link = book.css("h3 a::attr(href)").get()

            if link:
                yield response.follow(link, callback=self.parse_book)

        next_page = response.css("li.next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse_books)

    def parse_book(self, response):
        title = response.css('div.col-sm-6.product_main h1::text').get()
        table = response.css('table.table-striped')
        price = table.xpath("./tr[3]/td/text()").get()
        num_available = table.xpath("./tr[6]/td/text()").re("[0-9]+")
        if price:
            self.total_price += float(price[1:])
        if num_available:
            num_available = num_available[0]
        yield {"title": title,
               "price": price,
               "num_available": num_available,
               }

    def parse_quotes(self, response, **kwargs):
        for quote in response.css('div.quote'):
            text = quote.css('span.text::text').get()
            author = quote.css("small.author::text").get()
            tags = quote.css("div.tags a.tag::text").getall()
            yield {
                'text': text,
                'author': author,
                'tags': tags
            }

            t2 = response.css("li.next a::attr(href)").get()

            if t2:
                yield response.follow(url=t2, callback=self.parse)
