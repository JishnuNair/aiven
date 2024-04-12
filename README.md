# Aiven Senior Data Engineer Assignment

# Data Source
 [New York Taxi Dataset]!(https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)

This is a public dataset regarding taxi trips in New York, released as Parquet files. 

For the purpose of this assignment, I am only considering the Yellow and Green taxi data. The data dictionaries for these two datasets are available in the same link provided above.

# Data Pipeline

This is a Docker-based data pipeline that extracts data from a CSV file and loads it into a PostgreSQL database.

## How to Run

1. Build the Docker image: `docker build -t data-pipeline .`
2. Run the Docker container: `docker run -e DB_NAME=yourdbname -e DB_USER=yourdbuser -e DB_PASS=yourdbpass -e DB_HOST=yourdbhost -e DB_PORT=yourdbport data-pipeline`

## Design

The solution uses a Python script to load data from a CSV file, create a connection to the PostgreSQL database, create a table if it doesn't exist, and insert data into the table. It handles schema changes by checking the existing table schema against the incoming data schema and altering the table schema if necessary. The Python script is run inside a Docker container, with the necessary credentials passed as environment variables.