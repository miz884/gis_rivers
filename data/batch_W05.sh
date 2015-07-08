#!/bin/sh

function parse {
  echo "parsing ${1}..."
  target=$(basename ${1} | sed -e 's/_GML.zip/-g.xml/')
  unzip -c ${1} ${target} | python ./W05_parser.py
}
export -f parse

if [ -d /tmp/W05_river_path ]; then
  echo "/tmp/W05_river_path already exists."  >&2
  exit
fi
mkdir /tmp/W05_river_path

find . -type f -name 'W05*.zip' -exec bash -c "parse {}" \;


