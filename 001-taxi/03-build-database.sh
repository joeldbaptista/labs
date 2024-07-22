#!/bin/bash
set -e

duckdb db/taxi.db < sql/00.sql
