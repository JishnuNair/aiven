# Extracts parquet data for Yellow and Green taxi trips
# Sources:
# - Yellow taxi data:
#   https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-01.parquet
# - Green taxi data:
#   https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2024-01.parquet

import os
import time
import logging

import pandas as pd

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def load_data(url, retries=3, delay=2):
    """
    Load data from a URL with retries and delay
    Args:
        url (str): URL to load data from
        retries (int): Number of retries if loading data fails
        delay (int): Time to wait before retrying
    Returns:
        pd.DataFrame: Loaded data
    """
    for i in range(retries):
        try:
            logging.info("Attempting to load data from %s", url)
            data = pd.read_parquet(url)
            logging.info("Successfully loaded data from %s", url)
            return data
        except Exception as e:
            logging.error("Error loading data: %s", e)
            if i < retries - 1:  # i is zero indexed
                time.sleep(delay)  # wait before trying again
            else:
                raise Exception("Unable to load data from %s" % url) from e


def main():
    yellow_url = "https://d37ci6vzurychx.cloudfront.net/trip-data/" \
                 "yellow_tripdata_2024-01.parquet"
    green_url = "https://d37ci6vzurychx.cloudfront.net/trip-data/" \
                "green_tripdata_2024-01.parquet"

    yellow_data = load_data(yellow_url)
    green_data = load_data(green_url)

    # Create directory if not exists
    if not os.path.exists('data'):
        logging.info("Creating 'data' directory")
        os.makedirs('data')

    # Write data to parquet files
    logging.info("Writing yellow taxi data to parquet file")
    yellow_data.to_parquet('data/yellow_tripdata_2024-01.parquet')
    logging.info("Writing green taxi data to parquet file")
    green_data.to_parquet('data/green_tripdata_2024-01.parquet')


if __name__ == "__main__":
    main()
