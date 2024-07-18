#!/bin/bash
set -e

OWD=$(pwd)
VERSION=1.0.0

cd /tmp
wget https://github.com/duckdb/duckdb/releases/download/v$VERSION/duckdb_cli-linux-amd64.zip
sudo unzip duckdb_cli-linux-amd64.zip -d /usr/bin
sudo chmod 755 /usr/bin/duckdb && sudo chown joel:users /usr/bin/duckdb && cd $OWD
