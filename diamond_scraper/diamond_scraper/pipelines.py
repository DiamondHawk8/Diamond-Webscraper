# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import re
import logging


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
        self.items_processed = 0
        self.items_dropped = 0
        self.items_flagged = 0
        self.dropped_items = {}

    # TODO, allow for dynamic rules
    VALIDATION_RULES = {
        'tickerSymbol': lambda x: 0 < len(x) <= 5,
        'currency': lambda x: len(x) == 1,
        'price': lambda x: x >= 0,
        'volume': lambda x: x >= 0,
        'peRatio': lambda x: x > 0,
        'eps': lambda x: x >= 0,
    }

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # Logged after adapter transformation to ensure proper formatting
        spider.logger.debug(f"Raw item before {self.__class__.__name__} processing: {dict(adapter)}")

        for key, value in adapter.items():
            # Remove any None or empty values
            if value is None or value == "":
                raise DropItem(f"Invalid item {key}: {value}")

            if key in self.VALIDATION_RULES:
                # Numerically convert any
                if key in ['price', 'volume', 'peRatio', 'eps']:
                    try:
                        value = float(value)
                        adapter[key] = value
                    except ValueError:
                        spider.logger.error(f"Dropping item - {key}: {value}")
                        self.items_dropped += 1
                        raise DropItem(f"Invalid numeric value for {key}: {value}")
                if not self.VALIDATION_RULES[key](value):
                    spider.logger.warning(f"Suspicious value for {key}: {value}")
                    self.items_flagged += 1
        self.items_processed += 1
        return dict(adapter)


    def open_spider(self, spider):
        spider.logger.info(f"Starting {self.__class__.__name__} validation")

    def close_spider(self, spider):
        spider.logger.info(f"Finished {self.__class__.__name__} validation")
        spider.logger.info(f"Items processed: {self.items_processed}")
        spider.logger.info(f"Items dropped: {self.items_dropped}")
        spider.logger.info(f"Suspicious items: {self.items_flagged}")

        # Track spider wide statistics
        spider.crawler.stats.inc_value("custom/items_processed", count=self.items_processed)
        spider.crawler.stats.inc_value("custom/items_dropped", count=self.items_dropped)
        spider.crawler.stats.inc_value("custom/items_flagged", count=self.items_flagged)



