# Aiven Senior Data Engineer Assignment

# Data Source
 [New York Taxi Dataset](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)

This is a public dataset regarding taxi trips in New York, released as Parquet files. 

For the purpose of this assignment, I am only considering the Yellow and Green taxi data for 2024. The data dictionaries for these two datasets are available in the same link provided above.

# Data Pipeline

This is a Docker-based data pipeline that does the following steps:

* Extracts latest Taxi trips data for Yellow and Green trips
* Loads data to staging table in Postgres
* Loads data to final table in Postgres, after verifying schema changes

## How to Run

1. Build the Docker image: `docker build -t postgres-pipeline .`
2. Run the Docker container: `docker run -e DB_NAME=<DB_NAME> -e DB_USER=<DB_USER> -e DB_PASSWORD=<DB_PASSWORD> -e DB_HOST=<DB_HOST> -e DB_PORT=<DB_PORT> postgres_pipeline`

**Note:**
* To run specific sections of the pipeline, the following flags can be passed to `run.sh`
    * --extract-only
    * --stage-only
    * --final-only

## Design

