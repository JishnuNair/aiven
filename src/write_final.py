"""
Write final data to database
"""

import argparse
import logging

from sqlalchemy import create_engine
from sqlalchemy import MetaData, Table, func, text
from sqlalchemy.exc import ProgrammingError

from src.models import GreenTrips, YellowTrips

logging.basicConfig(level=logging.INFO)


def create_conn(db_name, db_user, db_pass, db_host, db_port):
    """
    Create a SQLAlchemy engine for a PostgreSQL database
    Args:
        db_name (str): Database name
        db_user (str): Database user
        db_pass (str): Database password
        db_host (str): Database host
        db_port (str): Database port
    Returns:
        sqlalchemy.engine.Engine: Engine connected to the database
    """
    try:
        logging.info("Creating database connection")
        db_url = (
            f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/"
            f"{db_name}"
        )
        engine = create_engine(db_url)
        logging.info("Successfully created database connection")
        return engine
    except Exception as e:
        logging.error("Failed to create database connection")
        logging.error(e)
        raise


def create_table(engine, table_name):
    # create yellow_trips or green_trips tables if they do not exist
    # handle schema changes by comparing with _stg_yellow_trips and 
    # _stg_green_trips
    # add insert_date and update_date columns to the final tables
    # add surrogate key to the final tables

    metadata = MetaData(engine)

    if table_name == "yellow_trips":
        table = YellowTrips.__table__
    elif table_name == "green_trips":
        table = GreenTrips.__table__
    else:
        raise ValueError("Invalid table name")
    
    try:
        table.create(engine)
        logging.info("Table %s created", table_name)
    except ProgrammingError:
        logging.info("Table %s already exists", table_name)

    # Check for schema changes
    stg_table_name = f"_stg_{table_name}"
    stg_table = Table(stg_table_name, metadata, autoload_with=engine)
    stg_columns = {col.name: col.type for col in stg_table.columns}
    final_columns = {col.name: col.type for col in table.columns
                     if col.name not in ["_id", "insert_date", "update_date"]}

    # Check for new columns
    new_columns = set(stg_columns.keys()) - set(final_columns.keys())
    for column in new_columns:
        # Updating the table object with the new column
        column_obj = getattr(stg_table.c, column)
        column_obj_copy = column_obj.copy()
        column_obj_copy.table = table
        column_obj_copy.create(table)
        # Add the new column to the final table
        engine.execute(text(f"ALTER TABLE {table_name} ADD COLUMN {column}"))
        logging.info("Column %s added to table %s", column, table_name)

    # Check for deleted columns
    deleted_columns = set(final_columns.keys()) - set(stg_columns.keys())
    for column in deleted_columns:
        rename_query = (
            f"ALTER TABLE {table_name} RENAME COLUMN {column} "
            f"TO {column}_archived"
        )
        engine.execute(text(rename_query))
        logging.info(
            "Column %s renamed to %s_archived in table %s",
            column,
            column,
            table_name,
        )

    # Check for columns with changed data types
    changed_columns = set(stg_columns.keys()).intersection(
        set(final_columns.keys())
    )
    for column in changed_columns:
        if stg_columns[column] != final_columns[column]:
            # Rename the old column
            rename_query = (
                f"ALTER TABLE {table_name} RENAME COLUMN {column} "
                f"TO {column}_archived"
            )
            engine.execute(text(rename_query))
            # Add the new column
            add_column_query = (
                f"ALTER TABLE {table_name} ADD COLUMN {column}"
            )
            engine.execute(text(add_column_query))
            logging.info(
                "Column %s in table %s had its data type changed",
                column,
                table_name,
            )

    logging.info("Table %s schema changes handled", table_name)


def insert_update_data(engine, table_name):
    """
    Insert or update data into the table in the database
    Args:
        engine (sqlalchemy.engine.Engine): Engine connected to the database
        table_name (str): Name of the table to insert/update data into
    """
    conn = engine.connect()
    metadata = MetaData(engine)
    stage_table_name = f"_stg_{table_name}"
    stage_table = Table(stage_table_name, metadata, autoload_with=engine)

    # Calculate the surrogate key for each record
    if table_name == 'yellow_trips':
        key_columns = ["VendorID", "tpep_pickup_datetime"]
    elif table_name == 'green_trips':
        key_columns = ["VendorID", "lpep_pickup_datetime"]
    else:
        raise ValueError(f"Unknown table: {table_name}")

    surrogate_key = func.hash(
        *[getattr(stage_table.c, col) for col in key_columns]
    )

    # Insert the new records into the table
    insert_query = (
        f"INSERT INTO {table_name} "
        f"SELECT * FROM {stage_table_name} "
        f"WHERE {surrogate_key} NOT IN "
        f"(SELECT surrogate_key FROM {table_name})"
    )
    conn.execute(text(insert_query))
    logging.info("Data inserted into table %s", table_name)

    # Update the existing records in the table
    update_query = (
        f"UPDATE {table_name} "
        f"SET "
        f"FROM {stage_table_name} "
        f"WHERE {table_name}.surrogate_key = {surrogate_key}"
    )
    conn.execute(text(update_query))
    logging.info("Data updated in table %s", table_name)


def main(args):
    db_name = args.db_name
    db_user = args.db_user
    db_pass = args.db_pass
    db_host = args.db_host
    db_port = args.db_port

    conn = create_conn(db_name, db_user, db_pass, db_host, db_port)

    create_table(conn, "yellow_trips")
    insert_update_data(conn, "yellow_trips")

    create_table(conn, "green_trips")
    insert_update_data(conn, "green_trips")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Write final data to database"
    )
    parser.add_argument(
        "--db_name",
        type=str,
        help="Database name",
        required=True
    )
    parser.add_argument(
        "--db_user",
        type=str,
        help="Database user",
        required=True
    )
    parser.add_argument(
        "--db_pass",
        type=str,
        help="Database password",
        required=True
    )
    parser.add_argument(
        "--db_host",
        type=str,
        help="Database host",
        required=True
    )
    parser.add_argument(
        "--db_port",
        type=str,
        help="Database port",
        required=True
    )

    args = parser.parse_args()
    main(args)
