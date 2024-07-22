#!/bin/bash
set -e

while IFS= read -r line; do
    echo "Pulling: $line (in the background)"
    wget -P ./data "$line" &
done < ./data/data.csv
