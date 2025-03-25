import sqlite3
from itemadapter import ItemAdapter
from diamond_scraper.utils import db_utils

class DatabasePipeline:
    """
    Pipeline to store items into a database.
    Uses SQLite by default. PostgreSQL support planned.
    """

    def __init__(self):
        self.connection = None
        self.cursor = None
        self.auto_create = True  # TODO Can be toggled in settings.py

    def open_spider(self, spider):
        """
        Establish database connection.
        - Load DB path from Scrapy settings or use default
        - Create a cursor for executing SQL
        """
        pass

    def close_spider(self, spider):
        """
        Commit any changes and close the database connection.
        """
        pass

    def process_item(self, item, spider):
        """
        For each item:
        - Ensure table exists (if auto_create is enabled)
        - Insert the item into the appropriate table
        """
        pass

    def insert_item_into(self, adapter, spider, table_name, auto_create=False):
        """
        Utility method for manually inserting an item into a specific table.
        """
        pass
