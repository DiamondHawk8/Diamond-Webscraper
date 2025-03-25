def generate_create_table(item, table_name=None):
    """
    Accepts an item or item adapter, and a name
    returns a CREATE TABLE IF NOT EXISTS
    checks the item name instance if a name is not provided
    """
    pass

def generate_insert_sql(item, table_name):
    """
    Returns INSERT INTO ... (columns) VALUES (?, ?, ...) and a tuple of values
    """
    pass

def initialize_table(cursor, item, table_name):
    """
    execution wrapper that:
    Checks if a table needs to be created
    Generates the SQL using generate_create_table_sql()
    Executes it using the provided cursor
    """
    pass

def insert_item(cursor, item, table_name):
    """
    execution wrapper that:
    Call generate_insert_sql( to build SQL and value tuple
    Execute the insert with the given DB cursor
    """
    pass


def log_db_action(spider, action, table, item=None):
    """
    Logs actions like table creation, inserts, errors, etc.
    """
    pass

def clear_table(cursor, table_name):
    pass

def get_existing_tables(cursor):
    pass