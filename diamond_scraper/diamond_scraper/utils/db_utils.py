from itemadapter import ItemAdapter
import sqlite3


def generate_create_table(item, table_name=None, override_types=None):
    """
    Accepts a Scrapy item or adapter and returns a SQL statement string:
    CREATE TABLE IF NOT EXISTS ...

    - Detects data types for fields if possible
    - Uses item class name as table name if none provided
    - Infers field type from instance, can be overridden if needed
    """

    adapter = ItemAdapter(item)

    if not table_name:
        table_name = item.__class__.__name__.lower()
    if not override_types:
        override_types = {}

    # Start Command structure
    command = f"CREATE TABLE IF NOT EXISTS {table_name}("

    for field_name, value in adapter.items():
        # Attempt type inference
        sql_type = "TEXT"
        if isinstance(value, bool):
            sql_type = "BOOLEAN"
        elif isinstance(value, int):
            sql_type = "INTEGER"
        elif isinstance(value, float):
            sql_type = "REAL"

        if field_name in override_types:
            sql_type = override_types[field_name]

        command += f"{field_name} {sql_type},"

    # Remove trailing comma and close command
    command = command[:-1] + ");"
    return command

    pass


def generate_insert_sql(item, table_name=None):
    """
    Returns (sql_string, values_tuple) for inserting the item into the specified table.

    (str, tuple):
        str: "INSERT INTO table_name (field1, field2, ...) VALUES (?, ?, ...)"
        tuple: (val1, val2, ...) extracted from item in the same order as columns.
    """
    if not table_name:
        table_name = item.__class__.__name__.lower()

    adapter = ItemAdapter(item)

    field_names = []
    values = []
    for field_name, value in adapter.items():
        field_names.append(field_name)
        values.append(value)

    columns = ", ".join(field_names)
    data = ", ".join(values)

    command = f"INSERT INTO {table_name} ({columns}) VALUES ({data});"

    return command, tuple(values)


def initialize_table(cursor, item, table_name, override_types=None):
    """
    Execution wrapper that:
    - Calls generate_create_table() to build table SQL
    - Executes the SQL using the provided DB cursor
    """
    pass


def insert_item(cursor, item, table_name, spider=None):
    """
    Execution wrapper that:
    - Calls generate_insert_sql() to build insert SQL + values
    - Executes insert using cursor
    - Optionally logs the result via log_db_action()
    """
    pass


def log_db_action(spider, action, table, item=None):
    """
    Logs a structured DB event for debugging/monitoring.

    Parameters:
    - action: INSERT, INSERT_FAILED, CREATE_TABLE etc
    - table: the target table name
    - item: optional Scrapy item (for type or summary)
    """
    pass


def clear_table(cursor, table_name):
    """
    Clears all contents from a table.

    TESTING ONLY, NO SAFETY CHECKS ENABLED
    """
    pass


def get_existing_tables(cursor):
    """
    Returns a list of existing table names from the connected databas
    """
    pass
