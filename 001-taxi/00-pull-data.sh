#!/bin/bash
set -e

while IFS= read -r line; do
    echo "Pulling: $line"
    wget -P ./data "$line"
done < ./data/data.csv
