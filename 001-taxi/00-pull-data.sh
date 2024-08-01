#!/bin/bash
set -e

while IFS= read -r line; do
    echo "Pulling: $line (in the background)"
    # redirect to null if you don't want to have the processes writing to stdout
    wget -P ./data "$line" & # > /dev/null
done < ./data/data.csv
