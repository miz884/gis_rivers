#!/bin/sh

function parse {
  echo "parsing ${1}..."
  target=$(basename ${1} | sed -e 's/_GML.zip/-g.xml/')
  unzip -c ${1} ${target} | python ./W05_parser.py
}
export -f parse

mkdir ./result/W05_river_path_data

find . -type f -name 'W05*.zip' -exec bash -c "parse {}" \;


