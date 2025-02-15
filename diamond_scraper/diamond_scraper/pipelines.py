# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import re


class DiamondScraperPipeline:
    def process_item(self, item, spider):

        adapter = ItemAdapter(item)

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
        return dict(adapter)


class DuplicatesPipeline:
    def __init__(self):
        self.timestamps_seen = set()

    def process_item(self, item, spider):

        adapter = ItemAdapter(item)

        adapter = ItemAdapter(item)
        if adapter["timestamp"] in self.timestamps_seen:
            raise DropItem(f"Item timestamp already seen: {adapter['timestamp']}")
        else:
            self.timestamps_seen.add(adapter["timestamp"])
            return dict(adapter)


class InvalidDataPipeline:
    # TODO, expand invalid item logic (check if fields within reasonable range?)
    def process_item(self, item, spider):

        adapter = ItemAdapter(item)

        for key, value in adapter.items():
            if value is None or value == "":
                raise DropItem(f"Invalid item {key}: {value}")

        return dict(adapter)
