import scrapy

from diamond_scraper.items import IntoliItem


class IntoliSpider(scrapy.Spider):
    name = 'IntoliSpider'
    urls = ["https://bot.sannysoft.com/"]

    def start_requests(self):
        for url in self.urls:
            self.logger.info(f"Beginning request for url: {url}")
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        """
        TODO FIELDS TO SCRAPE:
            ------------------------------------------General Tests
            userAgentTest = scrapy.Field()
            webDriverTest = scrapy.Field()
            webDriverAdvancedTest = scrapy.Field()
            chromeTest = scrapy.Field()
            permissionsTest = scrapy.Field()
            pluginsLengthTest = scrapy.Field()
            pluginTypeTest = scrapy.Field()
            languageTest = scrapy.Field()
            webGLVendorTest = scrapy.Field()
            webGlRendererTest = scrapy.Field()
            brokenImageDimensionsTest = scrapy.Field()
            ------------------------------------------PhantomJS Detection
            phantom_UATest = scrapy.Field()
            phantom_PROPERTIES = scrapy.Field()
            phantom_ETSL = scrapy.Field()
            phantom_LANGUAGE = scrapy.Field()
            phantom_WEBSOCKET = scrapy.Field()
            phantom_OVERFLOW = scrapy.Field()
            phantom_WINDOW_HEIGHT = scrapy.Field()
            ------------------------------------------Headless Chrome Detection
            headchr_UA = scrapy.Field()
            headchr_CHROME_OBJ = scrapy.Field()
            headchr_PERMISSIONS = scrapy.Field()
            headchr_PLUGINS = scrapy.Field()
            headchr_IFRAME = scrapy.Field()
            ------------------------------------------Debugging & Tool Detection
            chr_DEBUG_TOOLS = scrapy.Field()
            selenium_DRIVER = scrapy.Field()
            sequentum = scrapy.Field()
            ------------------------------------------Environment Data
            navigator = scrapy.Field()
            screen = scrapy.Field()
            battery = scrapy.Field()
            memory = scrapy.Field()
            ------------------------------------------Canvas Fingerprints
            canvas1 = scrapy.Field()
            canvas2 = scrapy.Field()
            canvas3 = scrapy.Field()
            canvas4 = scrapy.Field()
            canvas5 = scrapy.Field()
            ------------------------------------------Codec Support
            videoCodecs = scrapy.Field()
            audioCodecs = scrapy.Field()
            ------------------------------------------Fp-collect raw dump
            fp_collect = scrapy.Field()

        """

        webAgentTest = response.css()

        item = IntoliItem(
            webAgentTest=webAgentTest,
        )
        yield item
