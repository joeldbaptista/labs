-- 
DROP SCHEMA IF EXISTS reference CASCADE;
CREATE SCHEMA reference;

--
CREATE TABLE reference.files AS
SELECT *
FROM read_csv('data/data.csv', header=false, columns={'fname': 'TEXT'});

--
CREATE TABLE reference.time_buckets AS
SELECT '1 minutes' bucket, _start, _start + INTERVAL '1 minutes' _end
FROM (
    SELECT _start
    FROM generate_series(timestamp '2020-01-01', timestamp '2030-01-01', interval '1 minutes') t(_start)
) tt
UNION ALL
SELECT '5 minutes' bucket, _start, _start + INTERVAL '5 minutes' _end
FROM (
    SELECT _start
    FROM generate_series(timestamp '2020-01-01', timestamp '2030-01-01', interval '5 minutes') t(_start)
) tt
UNION ALL
SELECT '10 minutes' bucket, _start, _start + INTERVAL '10 minutes' _end
FROM (
    SELECT _start
    FROM generate_series(timestamp '2020-01-01', timestamp '2030-01-01', interval '10 minutes') t(_start)
) tt
UNION ALL
SELECT '30 minutes' bucket, _start, _start + INTERVAL '30 minutes' _end
FROM (
    SELECT _start
    FROM generate_series(timestamp '2020-01-01', timestamp '2030-01-01', interval '30 minutes') t(_start)
) tt
UNION ALL
SELECT '60 minutes' bucket, _start, _start + INTERVAL '60 minutes' _end
FROM (
    SELECT _start
    FROM generate_series(timestamp '2020-01-01', timestamp '2030-01-01', interval '60 minutes') t(_start)
) tt;


