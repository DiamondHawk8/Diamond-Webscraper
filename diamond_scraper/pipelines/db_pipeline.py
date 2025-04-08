import sqlite3
from diamond_scraper.utils import db_utils
import os


class DatabasePipeline:
    """
    Pipeline to store items into a database.
    Uses SQLite by default. PostgreSQL support planned.
    """

    def __init__(self):
        self.connection = None
        self.cursor = None
        self.auto_create = True  # TODO Can be toggled in settings.py
        self.backend = os.getenv("DB_BACKEND", "sqlite")

    def open_spider(self, spider):
        """
        Establish database connection.
        - Load DB path from Scrapy settings or use default
        - Create a cursor for executing SQL
        """
        db_path = spider.settings.get('DB_PATH', "DWS_scraper.db")
        self.connection = db_utils.get_db_connection(db_path=db_path)
        self.cursor = self.connection.cursor()

    def close_spider(self, spider):
        """
        Commit any changes and close the database connection.
        """
        self.connection.commit()
        self.connection.close()
        spider.logger.info('Database connection closed.')

    def process_item(self, item, spider):
        """
        For each item:
        - Ensure table exists (if auto_create is enabled)
        - Insert the item into the appropriate table
        """
        table_name = item.__class__.__name__.lower()

        if self.auto_create:
            db_utils.initialize_table(self.cursor, item, table_name)

        db_utils.insert_item(self.cursor, item, table_name, spider=spider)
        return item

    def insert_item_into(self, item, spider, table_name):
        """
        Utility method for manually inserting an item into a specific table.
        """
        db_utils.insert_item(self.cursor, item, table_name, backend=self.backend)

    def create_table(self, item, table_name=None):
        """
        Utility method for manually creating a table from an item.
        """
        db_utils.initialize_table(self.cursor, item, table_name)
