-- 
DROP SCHEMA IF EXISTS staging CASCADE;
CREATE SCHEMA staging;

-- source: https://duckdb.org/docs/data/parquet/overview.html
CREATE TABLE staging.yellow_tripdata AS
SELECT *, current_timestamp as load_dt
FROM read_parquet('data/*.parquet', filename=true, union_by_name=true);

