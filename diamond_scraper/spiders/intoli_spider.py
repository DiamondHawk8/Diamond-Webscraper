import scrapy
from diamond_scraper.items import IntoliItem
import diamond_scraper.utils.stealth_utils as stealth
import random
from scrapy_playwright.page import PageMethod
import time

# TODO, log database name to spider stats so that fine tuning can occur

class IntoliSpider(scrapy.Spider):
    name = 'IntoliSpider'
    urls = ["https://bot.sannysoft.com/"]

    def start_requests(self):
        for url in self.urls:
            headers = {"User-Agent": stealth.get_random_user_agent(skew=False)}
            self.logger.info(f"Beginning request for {url} with UA: {headers['User-Agent']}")
            print(f"Beginning request for {url} with UA: {headers['User-Agent']}")
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
                                         PageMethod("wait_for_timeout", stealth.get_random_wait_time())
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
        # TODO reorder fields, based on intoli
        # TODO implement detail scraping once <HIGH> functionality is implemented
        """
        TODO FIELDS TO SCRAPE:
            ------------------------------------------Environment Data
            navigatorTest = scrapy.Field()
            screenTest = scrapy.Field()
            ------------------------------------------Canvas Fingerprints
            canvas1Test = scrapy.Field()
            canvas2Test = scrapy.Field()
            canvas3Test = scrapy.Field()
            canvas4Test = scrapy.Field()
            canvas5Test = scrapy.Field()
            ------------------------------------------Codec Support
            audioCodecsTest = scrapy.Field()
            ------------------------------------------Fp-collect raw dump
            fpCollectDump = scrapy.Field()
        """

        def extract_general_table_elements(snippet, default=None):
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
        
        def extract_fingerprint_table_elements(snippet, default=None):
            result_cell = snippet.css('td:nth-child(2)')
            status = result_cell.css('::text').get()

            value_cell = snippet.css('td:nth-child(3)')
            value = value_cell.css('::text').get()
            return {
                "status": status if status else default,
                "value": value.strip() if value else default
            }


        generalTests = response.css('table tr')
        try:
            userAgentTest = extract_general_table_elements(generalTests[1])
            webDriverTest = extract_general_table_elements(generalTests[2])
            webDriverAdvancedTest = extract_general_table_elements(generalTests[3])
            chromeTest = extract_general_table_elements(generalTests[4])
            permissionsTest = extract_general_table_elements(generalTests[5])
            pluginsLengthTest = extract_general_table_elements(generalTests[6])
            pluginsTypeTest = extract_general_table_elements(generalTests[7])
            languageTest = extract_general_table_elements(generalTests[8])
            webGLVendorTest = extract_general_table_elements(generalTests[9])
            webGLRendererTest = extract_general_table_elements(generalTests[10])
            brokenImageDimensionsTest = extract_general_table_elements(generalTests[11])
        except Exception as e:
            self.logger.warning(f"Failed to extract general tests: {e}")
            return

        fingerprintTests = response.css('[id=fp2] tr')
        try:
            phantomUaTest = extract_fingerprint_table_elements(fingerprintTests[0])
            phantomPropertiesTest = extract_fingerprint_table_elements(fingerprintTests[1])
            phantomEtslTest = extract_fingerprint_table_elements(fingerprintTests[2])
            phantomLanguageTest = extract_fingerprint_table_elements(fingerprintTests[3])
            phantomWebsocketTest = extract_fingerprint_table_elements(fingerprintTests[4])
            MQ_ScreenTest = extract_fingerprint_table_elements(fingerprintTests[5])
            phantomOverflowTest = extract_fingerprint_table_elements(fingerprintTests[6])
            phantomWindowHeightTest = extract_fingerprint_table_elements(fingerprintTests[7])
            headchrUaTest = extract_fingerprint_table_elements(fingerprintTests[8])
            headchrChromeObjTest = extract_fingerprint_table_elements(fingerprintTests[9])
            headchrPermissionsTest = extract_fingerprint_table_elements(fingerprintTests[10])
            headchrPluginsTest = extract_fingerprint_table_elements(fingerprintTests[11])
            headchrIframeTest = extract_fingerprint_table_elements(fingerprintTests[12])
            chromeDebugToolsTest = extract_fingerprint_table_elements(fingerprintTests[13])
            seleniumDriverTest = extract_fingerprint_table_elements(fingerprintTests[14])
            batteryTest = extract_fingerprint_table_elements(fingerprintTests[15])
            memoryTest = extract_fingerprint_table_elements(fingerprintTests[16])
            transparentPixelTest = extract_fingerprint_table_elements(fingerprintTests[17])
            sequentumTest = extract_fingerprint_table_elements(fingerprintTests[18])
            videoCodecsTest = extract_fingerprint_table_elements(fingerprintTests[19])
        except Exception as e:
            self.logger.warning(f"Failed to extract fingerprint tests: {e}")
            return

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

            phantomUaTest=phantomUaTest,
            phantomPropertiesTest=phantomPropertiesTest,
            phantomEtslTest=phantomEtslTest,
            phantomLanguageTest=phantomLanguageTest,
            phantomWebsocketTest=phantomWebsocketTest,
            MQ_ScreenTest=MQ_ScreenTest,
            phantomOverflowTest=phantomOverflowTest,
            phantomWindowHeightTest=phantomWindowHeightTest,
            headchrUaTest=headchrUaTest,
            headchrChromeObjTest=headchrChromeObjTest,
            headchrPermissionsTest=headchrPermissionsTest,
            headchrPluginsTest=headchrPluginsTest,
            headchrIframeTest=headchrIframeTest,
            chromeDebugToolsTest=chromeDebugToolsTest,
            seleniumDriverTest=seleniumDriverTest,
            batteryTest=batteryTest,
            memoryTest=memoryTest,
            transparentPixelTest=transparentPixelTest,
            sequentumTest=sequentumTest,
            videoCodecsTest=videoCodecsTest,
        )
        yield item
