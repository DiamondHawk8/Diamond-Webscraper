# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import re
import logging


class DiamondScraperPipeline:

    # Generalized pipeline for testing and development purposes, will be removed/replaced with modular pipeline
    def process_item(self, item, spider):
        spider.logger.info("Beginning Diamond Scraper pipeline")
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
        spider.logger.info("Items processed")
        return dict(adapter)


class DuplicatesPipeline:
    def __init__(self):
        self.timestamps_seen = set()

    def process_item(self, item, spider):
        spider.logger.info("Beginning duplicate data check")
        adapter = ItemAdapter(item)

        # Logged after adapter transformation to ensure proper formatting
        spider.logger.debug(f"Raw item before {self.__class__.__name__} processing: {dict(adapter)}")

        adapter = ItemAdapter(item)
        if adapter["timestamp"] in self.timestamps_seen:
            spider.logger.warning(f"Item timestamp already seen: {adapter['timestamp']}")
            raise DropItem(f"Item timestamp already seen: {adapter['timestamp']}")
        else:
            self.timestamps_seen.add(adapter["timestamp"])
            return dict(adapter)


class InvalidDataPipeline:

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
        spider.logger.info(f"Starting InvalidDataPipeline validation")
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
                        raise DropItem(f"Invalid numeric value for {key}: {value}")
                if not self.VALIDATION_RULES[key](value):
                    spider.logger.warning(f"Suspicious value for {key}: {value}")

        return dict(adapter)
