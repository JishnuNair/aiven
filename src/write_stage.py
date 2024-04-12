"""
Loads extracted parquet files to staging tables in PostgreSQL
Postgres connection details are taken as input arguments
The staging tables are created if they do not exist
staging table names are _stg_yellow_trips and _stg_green_trips
"""

import argparse
import logging

import pandas as pd
from sqlalchemy import create_engine

logging.basicConfig(level=logging.INFO)


def load_data(file_path):
    """
    Load data from a parquet file
    Args:
        file_path (str): Path to the parquet file
    Returns:
        pd.DataFrame: Loaded data
    """
    logging.info("Loading data from %s", file_path)
    data = pd.read_parquet(file_path)
    return data


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


def create_and_insert_data(engine, table_name, data, chunksize=1000):
    """
    Create a table in the database and insert data into it in chunks
    Args:
        engine (sqlalchemy.engine.Engine): Engine connected to the database
        table_name (str): Name of the table to create and insert data into
        data (pandas.DataFrame): DataFrame containing the data
        chunksize (int): Number of rows to insert at a time
    """
    logging.info("Creating and inserting data into table %s", table_name)
    data.to_sql(
        table_name,
        engine,
        if_exists='replace',
        index=False,
        chunksize=chunksize
    )


def main(args):
    yellow_file_path = args.yellow_file_path
    green_file_path = args.green_file_path
    db_name = args.db_name
    db_user = args.db_user
    db_pass = args.db_pass
    db_host = args.db_host
    db_port = args.db_port

    conn = create_conn(db_name, db_user, db_pass, db_host, db_port)

    yellow_data = load_data(yellow_file_path)
    create_and_insert_data(
        conn, "_stg_yellow_trips", yellow_data, chunksize=1000
    )

    green_data = load_data(green_file_path)
    create_and_insert_data(
        conn, "_stg_green_trips", green_data, chunksize=1000
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-y",
        "--yellow_file_path",
        help="Path to yellow trips parquet file",
        required=True
    )
    parser.add_argument(
        "-g",
        "--green_file_path",
        help="Path to green trips parquet file",
        required=True
    )
    parser.add_argument(
        "-dbn",
        "--db_name",
        help="PostgreSQL database name",
        required=True
    )
    parser.add_argument(
        "-dbu",
        "--db_user",
        help="PostgreSQL database user",
        required=True
    )
    parser.add_argument(
        "-dbp",
        "--db_pass",
        help="PostgreSQL database password",
        required=True
    )
    parser.add_argument(
        "-dbh",
        "--db_host",
        help="PostgreSQL database host",
        required=True
    )
    parser.add_argument(
        "-dbt",
        "--db_port",
        help="PostgreSQL database port",
        required=True
    )
    args = parser.parse_args()
    main(args)
