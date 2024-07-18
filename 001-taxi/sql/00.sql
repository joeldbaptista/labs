-- 
DROP SCHEMA IF EXISTS staging CASCADE;
CREATE SCHEMA staging;

-- source: https://duckdb.org/docs/data/parquet/overview.html
CREATE TABLE staging.yellow_tripdata AS
SELECT *
FROM read_parquet('data/*.parquet', filename=TRUE);
