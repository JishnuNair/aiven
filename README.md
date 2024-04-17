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
All stages of the pipeline are run by default. 

* To run specific sections of the pipeline, the following flags can be passed to `run.sh`, and the image built again.
    * --extract-only
    * --stage-only
    * --final-only

## Design

### Extract

The parquet files for Yellow and Green taxi trips are extracted to pandas dataframes, and written to respective parquet files under data directory.

### Load

There are two sub-steps in the load process, with the data being loaded to stage tables first, and then processed before loading to final tables.

#### Step 1: Write to stage table

The parquet files are read to pandas Dataframes, and written to stage tables in Postgres database. The tables are replaced during each run, and the load happens in batches. 

#### Step 2: Write to final table

The final tables are not replaced during every run. The data loaded to stage tables is processed first before loading only the incremental records to the final tables. 

These are the stages in this step:

* **Cleaning**: Duplicate records are removed from both tables, by checking using the key columns for each table. Fare adjustments are the main reason for duplicate records, and duplicates were removed by choosing the record with valid fares. 

* **Schema Validation**: The schema of stage and final tables are compared, and actions taken depending on the differences.
    * In case of field additions, the new field is added to the final table using alter statements
    * In case of field deletions, the deleted fields are renamed by appending "_archive" to the column name
    * In case of changes to data types, the existing columns are first renamed by appending "_archive", and new column created with updated data type

* **Insert/Update**: After the schema validation and updates are performed, the records are inserted/updated to final table
    * Inserts: Incremental records are identified by calculating the hash of key columns in each table. The new records are inserted to final table, and `insert_date` column populated
    * Updates: In case of updates to existing records, the respective fields are updated, and `update_date` populated. Updates are not implemented in the code currently. 