def generate_create_table(item, table_name=None):
    """
    Accepts an item or item adapter, and a name
    returns a CREATE TABLE IF NOT EXISTS
    checks the item name instance if a name is not provided
    """

def generate_insert_sql(item, table_name):
    """
    Returns INSERT INTO ... (columns) VALUES (?, ?, ...) and a tuple of values
    """

def initialize_table(cursor, item, table_name):
    """TBD"""

