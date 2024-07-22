#!/bin/bash
set -e

python3 src/extract_yellow_taxi_data_links.py > data/data.csv
