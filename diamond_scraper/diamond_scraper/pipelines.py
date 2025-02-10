# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import re


class DiamondScraperPipeline:

    def open_spider(self, spider):
        self.file = open('data.json', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):

        if not isinstance(item, ItemAdapter):
            adapter = ItemAdapter(item)
        else:
            adapter = item

        for key, value in adapter.items():
            adapter.update({key: value.lower().strip().replace(' ', '_')})

        # Remove leading currency symbol in open and eps (is there a simpler way to do this)
        currency = adapter['currency']
        adapter.update({'open': adapter['open'][adapter['open'].index(currency) + 1:]})
        adapter.update({'eps': adapter['eps'][adapter['eps'].index(currency) + 1:]})

        # Remove leading 'Volume: ' string in volume value
        adapter.update({'volume': adapter['volume'][adapter['volume'].index(':') + 2:]})
        for key, value in adapter.items():
            print(key, value)
        return dict(adapter)


class DuplicatesPipeline:
    def __init__(self):
        self.timestamps_seen = set()

    def process_item(self, item, spider):

        if not isinstance(item, ItemAdapter):
            adapter = ItemAdapter(item)
        else:
            adapter = item

        adapter = ItemAdapter(item)
        if adapter["timestamp"] in self.timestamps_seen:
            raise DropItem(f"Item timestamp already seen: {adapter['timestamp']}")
        else:
            self.timestamps_seen.add(adapter["timestamp"])
            return dict(adapter)


class InvalidDataPipeline:
    # TODO, expand invalid item logic (check if fields within reasonable range?)
    def process_item(self, item, spider):
        print("FINAL --------------------------------",item)
        if not isinstance(item, ItemAdapter):
            adapter = ItemAdapter(item)
        else:
            adapter = item

        for key, value in adapter.items():
            if key is None or value is None:
                raise DropItem(f"Invalid item {key}: {value}")

        return dict(adapter)