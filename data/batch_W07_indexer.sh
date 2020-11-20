#!/bin/sh

function parse {
  echo "parsing ${1}..."
  target=$(basename ${1} | sed -e 's/\([0-9]\).csv/\1/')
  python2 ./W07_indexer.py ${target}
}
export -f parse

find result/W07_river_mesh/ -type f -name '*.csv' -exec bash -c "parse {}" \;

