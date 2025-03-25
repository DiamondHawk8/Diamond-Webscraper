import sqlite3
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

class DatabasePipeline:
    """
    Generic database pipeline for writing validated items to a persistent store.
    Currently uses SQLite, planned to support postgreSQL later
    """

    def __init__(self):
        self.connection = None
        self.cursor = None

    def open_spider(self, spider):
        """
        Initialize database connection and tables when spider opens.
        Read config from settings or environment variables.
        """
        # TODO: Read database path or URI from settings
        # TODO: Connect to SQLite using sqlite3.connect(...)
        # TODO: Create tables for StockItem and IntoliItem if they don't exist
        pass

    def close_spider(self, spider):
        """
        Commit transactions and close the database connection.
        """
        # TODO: self.connection.commit() and self.connection.close()
        pass

    def process_item(self, item, spider):
        """
        Route item to appropriate insert logic based on type.
        """
        adapter = ItemAdapter(item)

        # TODO: Identify item type and call self.insert_item_...()
        # TODO: replace with more robust functionality

        return item

    def insert_item_stock(self, adapter, spider):
        """
        Insert a StockItem into the database.
        """
        # TODO: Define and execute INSERT INTO query for stock table
        pass

    def insert_item_intoli(self, adapter, spider):
        """
        Insert an IntoliItem into the database.
        """
        # TODO: Define and execute INSERT INTO query for intoli table
        pass

    def insert_item_into(self, adapter, spider, database, auto_create=False):
        """
        Insert an Item into a specified database
        Additionally allows for attempting automatic database creation
        """
        # TODO: Create a utils class to handle more advanced operations

