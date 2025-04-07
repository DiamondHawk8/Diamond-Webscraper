
import scrapy
from diamond_scraper.items import IntoliItem
import diamond_scraper.utils.stealth_utils as stealth
import random
from scrapy_playwright.page import PageMethod
import time

class IntoliSpider(scrapy.Spider):
    name = 'IntoliSpider'
    urls = ["https://bot.sannysoft.com/"]

    def start_requests(self):
        for url in self.urls:
            headers = {"User-Agent": stealth.get_random_user_agent()}
            self.logger.info(f"Beginning request for {url} with UA: {headers['User-Agent']}")
            self.logger.info(f"Beginning request for {url}")
            yield scrapy.Request(url=url,
                                 callback=self.parse,
                                 headers=headers,
                                 meta={
                                     "playwright": True,
                                     "playwright_page_methods": [
                                         # Remove webdriver
                                         # TODO WebGL spoofing, stack trace tampering, property descriptor traps
                                         PageMethod("add_init_script", """
                                         Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                                         Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
                                         Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3] });
                                         window.chrome = { runtime: {} };
                                         """),
                                         PageMethod('wait_for_selector', 'body'),
                                         PageMethod(
                                             "wait_for_function",
                                             "document.querySelector('#fp2') && document.querySelector('#fp2').rows.length > 2"
                                         ),
                                         PageMethod("wait_for_timeout", 30000) # Debug, should not be set this high for general purpsoes
                                     ]
                                 }
                                 )

            # POST request for testing
            """
            yield scrapy.FormRequest(
                url="https://httpbin.org/post",
                formdata={"test": "val"},
                meta={"playwright": True},
            )
            """

    def parse(self, response):
        print("arrived at parse")
        self.logger.info("[INTOLI] Playwright rendering triggered.")
        print(f"[DEBUG] Rendered response length: {len(response.text)}")
        """
        TODO FIELDS TO SCRAPE:
            ------------------------------------------PhantomJS Detection
            phantomUaTest = scrapy.Field()
            phantomPropertiesTest = scrapy.Field()
            phantomEtslTest = scrapy.Field()
            phantomLanguageTest = scrapy.Field()
            phantomWebsocketTest = scrapy.Field()
            MQ_ScreenTest = scrapy.Field()
            phantomOverflowTest = scrapy.Field()
            phantomWindowHeightTest = scrapy.Field()
            ------------------------------------------Headless Chrome Detection
            headchrUaTest = scrapy.Field()
            headchrChromeObjTest = scrapy.Field()
            headchrPermissionsTest = scrapy.Field()
            headchrPluginsTest = scrapy.Field()
            headchrIframeTest = scrapy.Field()
            ------------------------------------------Debugging & Tool Detection
            chromeDebugToolsTest = scrapy.Field()
            seleniumDriverTest = scrapy.Field()
            sequentumTest = scrapy.Field()
            ------------------------------------------Environment Data
            navigatorTest = scrapy.Field()
            screenTest = scrapy.Field()
            batteryTest = scrapy.Field()
            memoryTest = scrapy.Field()
            ------------------------------------------Canvas Fingerprints
            canvas1Test = scrapy.Field()
            canvas2Test = scrapy.Field()
            canvas3Test = scrapy.Field()
            canvas4Test = scrapy.Field()
            canvas5Test = scrapy.Field()
            ------------------------------------------Codec Support
            videoCodecsTest = scrapy.Field()
            audioCodecsTest = scrapy.Field()
            ------------------------------------------Fp-collect raw dump
            fpCollectDump = scrapy.Field()
        """

        def extract_table_elements(snippet, default=None):
            """
            Extracts test status and value from a <tr> snippet.
            Returns a dict with 'status' and 'value' keys.
            """
            result_cell = snippet.css('td:nth-child(2)')
            status_class = result_cell.attrib.get('class', '').strip()

            value = result_cell.css('::text').get()
            return {
                "status": status_class if status_class else default,
                "value": value.strip() if value else default
            }

        generalTests = response.css('table tr')
        try:
            userAgentTest = extract_table_elements(generalTests[1])
            webDriverTest = extract_table_elements(generalTests[2])
            webDriverAdvancedTest = extract_table_elements(generalTests[3])
            chromeTest = extract_table_elements(generalTests[4])
            permissionsTest = extract_table_elements(generalTests[5])
            pluginsLengthTest = extract_table_elements(generalTests[6])
            pluginsTypeTest = extract_table_elements(generalTests[7])
            languageTest = extract_table_elements(generalTests[8])
            webGLVendorTest = extract_table_elements(generalTests[9])
            webGLRendererTest = extract_table_elements(generalTests[10])
            brokenImageDimensionsTest = extract_table_elements(generalTests[11])
        except Exception as e:
            self.logger.warning(f"Failed to extract general tests: {e}")
            return

        # TODO implement Playwright so that fingerprint scanner tests can be scraped
        fingerprintTests = response.css('[id=fp2] tr')
        try:



        print("---------------------------------------------------------------------------------------")
        print(fingerprintTests)

        # print(response.body)



        item = IntoliItem(
            userAgentTest=userAgentTest,
            webDriverTest=webDriverTest,
            webDriverAdvancedTest=webDriverAdvancedTest,
            chromeTest=chromeTest,
            permissionsTest=permissionsTest,
            pluginsLengthTest=pluginsLengthTest,
            pluginsTypeTest=pluginsTypeTest,
            languageTest=languageTest,
            webGLVendorTest=webGLVendorTest,
            webGLRendererTest=webGLRendererTest,
            brokenImageDimensionsTest=brokenImageDimensionsTest,
        )
        print(dict(item))
        yield item
