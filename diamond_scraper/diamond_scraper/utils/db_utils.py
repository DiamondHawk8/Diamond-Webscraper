import traceback

from itemadapter import ItemAdapter
import sqlite3
import json

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
        # Handle dicts/lists by JSON-encoding them
        if isinstance(value, (dict, list)):
            value = json.dumps(value)
        values.append(value)

    columns = ", ".join(field_names)
    placeholders = ", ".join(["?"] * len(values))
    command = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders});"

    return command, tuple(values)



def initialize_table(cursor, item, table_name=None, override_types=None, spider=None):
    """
    Ensures the table exists for this item by:
    1. Building the CREATE TABLE IF NOT EXISTS statement via generate_create_table()
    2. Executing it with 'cursor.execute(...)'

    Args:
        cursor: The sqlite3 (or Postgres) cursor object with .execute() method.
        item: The item or adapter representing the schema.
        table_name: The SQL table name to create if missing.
        override_types: Dict for manually overriding certain field types
    """
    command = generate_create_table(item, table_name, override_types)
    try:
        cursor.execute(command)
        log_db_action(spider, "CREATE_TABLE", table_name, item=item)
    except Exception as e:
        log_db_action(spider, "CREATE_TABLE_FAILED", table_name, item=item, error=e)
        raise


def insert_item(cursor, item, table_name, spider=None, log=True):
    """
    Execution wrapper that:
    - Calls generate_insert_sql() to build insert SQL + values
    - Executes insert using cursor
    - Optionally logs the result via log_db_action()
    """
    sql, vals = generate_insert_sql(item, table_name)
    try:
        cursor.execute(sql, vals)
        if log:
            log_db_action(spider, "INSERT_ITEM", table_name, item=item)
    except Exception as e:
        if log:
            log_db_action(spider, "INSERT_FAILED", table_name, item=item, error=e)
        raise


def log_db_action(spider, action, table, item=None, error=None):
    """
    Logs a structured DB event for debugging/monitoring.

    Parameters:
    - action: INSERT, INSERT_FAILED, CREATE_TABLE etc
    - table: the target table name
    - item: optional Scrapy item (for type or summary)
    """
    msg = f"[DB:{action}] table={table}"
    if item:
        msg += f" item={item.__class__.__name__}"
    if spider and hasattr(spider, 'logger'):
        if not error:
            spider.logger.info(msg)
        else:
            spider.logger.error(f"{msg}\nException: {error})")
    else:
        if not error:
            print(msg)
        else:
            print(f"{msg}\nException: {error}")


def clear_table(cursor, table_name, spider=None):
    """
    Clears all contents from a table.

    TESTING ONLY, NO SAFETY CHECKS ENABLED
    """
    cursor.execute(f"DELETE FROM {table_name}")
    spider.logger.info(f"Clearing table {table_name}")
    pass

def drop_table(cursor, table_name, spider=None):
    """
    Drops specified table

    TESTING ONLY, NO SAFETY CHECKS ENABLED
    """
    cursor.execute(f"DROP TABLE {table_name}")
    spider.logger.info(f"Dropped table {table_name}")

def get_existing_tables(cursor):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    return [row[0] for row in cursor.fetchall()]
