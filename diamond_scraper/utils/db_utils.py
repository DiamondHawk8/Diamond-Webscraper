import traceback

from itemadapter import ItemAdapter
import sqlite3
import psycopg2
import json
import os
import traceback
import logging

logger = logging.getLogger(__name__)


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


def generate_insert_sql(item, table_name=None, backend="sqlite"):
    """
    Returns (sql_string, values_tuple) for inserting the item into the specified table.

    For sqlite: uses "?" placeholders
    For postgres: uses "%s" placeholders
    """
    if not table_name:
        table_name = item.__class__.__name__.lower()

    adapter = ItemAdapter(item)
    field_names = []
    values = []

    for field_name, value in adapter.items():
        field_names.append(field_name)
        # JSON-encode if dict or list
        if isinstance(value, (dict, list)):
            value = json.dumps(value)
        values.append(value)

    columns = ", ".join(field_names)

    # Choose placeholders
    if backend == "postgres":
        placeholders = ", ".join(["%s"] * len(values))
    else:  # Default to sqlite
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


def insert_item(cursor, item, table_name, spider=None, log=True, backend="sqlite"):
    """
    Execution wrapper that:
    - Calls generate_insert_sql() to build insert SQL + values
    - Executes insert using cursor
    - Optionally logs the result via log_db_action()
    """
    sql, vals = generate_insert_sql(item, table_name, backend=backend)
    try:
        cursor.execute(sql, vals)
        if log:
            log_db_action(spider, "INSERT_ITEM", table_name, item=item)
    except Exception as e:
        if log:
            log_db_action(spider, "INSERT_FAILED", table_name, item=item, error=e)


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
    if spider:
        spider.logger.info(f"Clearing table {table_name}")
    pass


def drop_table(cursor, table_name, spider=None):
    """
    Drops specified table

    TESTING ONLY, NO SAFETY CHECKS ENABLED
    """
    cursor.execute(f"DROP TABLE {table_name}")
    if spider:
        spider.logger.info(f"Dropped table {table_name}")


def get_existing_tables(cursor):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    return [row[0] for row in cursor.fetchall()]


def get_db_connection(db_path=None):
    """
    Open a database connection based on the DB_BACKEND environment variable.

    Usage:
        connection = get_db_connection()
        # connection is either an SQLite or PostgreSQL connection object.

    Environment Variables:
        DB_BACKEND (str): "sqlite" or "postgres"

    For PostgreSQL
        DB_HOST (str): Host of the PostgreSQL server
        DB_PORT (str): Port number for PostgreSQL
        DB_NAME (str): Database name
        DB_USER (str): Username
        DB_PASSWORD (str): Password

    Returns:
        A connection object for the selected database backend.
    """

    # fallback to "sqlite" if unset
    db_backend = os.getenv("DB_BACKEND", "sqlite")

    if db_backend == "postgres":
        logger.info("Using PostgreSQL database")
        try:
            conn = psycopg2.connect(
                host=os.getenv("DB_HOST", "localhost"),
                port=os.getenv("DB_PORT", "5432"),
                dbname=os.getenv("DB_NAME", "DWS_db"),
                user=os.getenv("DB_USER", "postgres"),
                password=os.getenv("DB_PASSWORD", "secret")
            )
            conn.autocommit = True
            return conn
        except Exception as e:
            logger.error("Unable to connect to PostgreSQL database")
            traceback.print_exc()
            raise e  # or sys.exit(1), or some graceful fallback

    elif db_backend == "sqlite":
        print("Using SQLite database")
        if db_path:
            connection = sqlite3.connect(db_path)
        else:
            connection = sqlite3.connect("DWS_scraper.db")
        return connection
    else:
        logger.warning(f"Unknown DB_BACKEND='{db_backend}', defaulting to SQLite file='DWS_scraper.db'")
        try:
            connection = sqlite3.connect("DWS_scraper.db")
            return connection
        except Exception as e:
            logger.error("Unable to connect to SQLite database")
            traceback.print_exc()


