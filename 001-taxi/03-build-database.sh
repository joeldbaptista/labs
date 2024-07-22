#!/bin/bash
set -e

duckdb db/taxi.db < sql/00.sql
duckdb db/taxi.db < sql/01.sql
duckdb db/taxi.db < sql/02.sql
