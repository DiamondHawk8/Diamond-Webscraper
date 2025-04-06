# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from diamond_scraper.utils import validation_logger


class DiamondScraperPipeline:

    def __init__(self):
        self.items_processed = 0

    # Generalized pipeline for testing and development purposes, will be removed/replaced with modular pipeline
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # Logged after adapter transformation to ensure proper formatting
        spider.logger.debug(f"Raw item before {self.__class__.__name__} processing: {dict(adapter)}")

        for key, value in adapter.items():
            adapter.update({key: value.lower().strip().replace(' ', '_')})

        # Remove leading currency symbol in open and eps
        if "currency" in adapter:
            currency = adapter["currency"]
            if "open" in adapter and currency in adapter["open"]:
                adapter["open"] = adapter["open"][adapter["open"].index(currency) + 1:]
            if "eps" in adapter and currency in adapter["eps"]:
                adapter["eps"] = adapter["eps"][adapter["eps"].index(currency) + 1:]

        # Remove leading 'Volume: ' string in volume value
        if "volume" in adapter and ":" in adapter["volume"]:
            adapter["volume"] = adapter["volume"].split(":")[1].strip()
        for key, value in adapter.items():
            print(key, value)
        self.items_processed += 1
        return dict(adapter)

    def open_spider(self, spider):
        spider.logger.info(f"Starting {self.__class__.__name__} validation")

    def close_spider(self, spider):
        spider.logger.info(f"Finished {self.__class__.__name__} validation")
        spider.logger.info(f"Items processed: {self.items_processed}")

        spider.crawler.stats.inc_value("custom/items_processed", count=self.items_processed)


class DuplicatesPipeline:
    def __init__(self):
        self.timestamps_seen = set()
        self.items_processed = 0
        self.items_dropped = 0
        self.dropped_items = {}

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # Logged after adapter transformation to ensure proper formatting
        spider.logger.debug(f"Raw item before {self.__class__.__name__} processing: {dict(adapter)}")

        adapter = ItemAdapter(item)
        if adapter["timestamp"] in self.timestamps_seen:
            spider.logger.warning(f"Item timestamp already seen: {adapter['timestamp']}")
            self.items_dropped += 1
            raise DropItem(f"Item timestamp already seen: {adapter['timestamp']}")
        else:
            self.timestamps_seen.add(adapter["timestamp"])
            return dict(adapter)

    def open_spider(self, spider):
        spider.logger.info(f"Starting {self.__class__.__name__} validation")

    def close_spider(self, spider):
        spider.logger.info(f"Finished {self.__class__.__name__} validation")
        spider.logger.info(f"Items processed: {self.items_processed}")
        spider.logger.info(f"Duplicate items dropped: {self.items_dropped}")

        spider.crawler.stats.inc_value("custom/items_processed", count=self.items_processed)
        spider.crawler.stats.inc_value("custom/items_dropped", count=self.items_dropped)


class InvalidDataPipeline:
    def __init__(self):
        self.validation_logger = None  # Must be initialized after pipeline init, as spider does not exist yet
        self.validation_rules = {
            "tickerSymbol": lambda x: (0 < len(x) <= 5, x),
            "currency": lambda x: (len(x) == 1, x),
            "price": lambda x: (float(x) >= 0, x),
            "volume": lambda x: (float(x) >= 0, x),
            "peRatio": lambda x: (float(x) > 0, x),
            "eps": lambda x: (float(x) >= 0, x),
        }

    def open_spider(self, spider):
        self.validation_logger = validation_logger.ValidationLogger(spider, enable_logging=True)
        spider.logger.info(f"Starting {self.__class__.__name__} validation")

    def process_item(self, item, spider):
        try:
            return self.validation_logger.process_item(item, self.validation_rules)
        except DropItem as e:
            spider.logger.warning(str(e))
            raise

    def close_spider(self, spider):
        spider.logger.info(f"Finished {self.__class__.__name__} validation")

class TestPipeline:
    def __init__(self):
        self.validation_logger = None

    def open_spider(self, spider):
        self.validation_logger = validation_logger.ValidationLogger(spider, enable_logging=True, logging_rules={
            "ITEM_INPUT": {"log": True, "level": "info"},
            "ITEM_OUTPUT": {"log": True, "level": "info"},
            "FIELD_FAILURE": {"log": True, "level": "warning"},
            "FIELD_FLAGGED": {"log": True, "level": "warning"},
            "ITEM_FAILURE": {"log": True, "level": "error"},
            "ITEM_DROPPED": {"log": True, "level": "error"},
        })
        spider.logger.info(f"Starting {self.__class__.__name__} validation")

    def process_item(self, item, spider):
        test_item = {
            "tickerSymbol": " tesla ",  # Should be cleaned (uppercase, stripped spaces)
            "currency": "USD",  # Valid
            "price": -5,  # Invalid (negative price)
            "volume": "N/A",  # Invalid (non-numeric)
            "peRatio": 15.3,  # Valid
            "eps": 0.02,  # Suspicious (below 0.05 threshold)
        }

        test_rules = {
            "tickerSymbol": lambda x: (True, x.upper().strip()),  # Convert to uppercase, strip spaces
            "currency": lambda x: (len(x) == 3, x),  # Ensure it's a 3-letter currency code
            "price": lambda x: (x >= 0, x),  # Fail if price is negative
            "volume": lambda x: (x.isdigit(), int(x) if x.isdigit() else x),  # Fail if non-numeric
            "peRatio": lambda x: (x > 0, x),  # Must be positive
            "eps": lambda x: (None if x < 0.05 else True, x),  # Flag as suspicious if below 0.05
        }

        try:
            return self.validation_logger.process_item(test_item, test_rules)
        except DropItem as e:
            spider.logger.warning(str(e))
            raise

    def close_spider(self, spider):
        spider.logger.info(f"Finished {self.__class__.__name__} validation")