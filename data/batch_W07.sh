#!/bin/sh

TO_PATH=./result/W07_river_mesh/

function parse {
  echo "parsing ${1}..."
  target=$(basename ${1} | sed -e 's/_GML.zip/.xml/')
  result=$(basename ${1} | sed -e 's/W07-[0-9]*_//; s/-jgd_GML.zip/.csv/')
  unzip -c ${1} ${target} "*/${target}"| python ./W07_parser.py > ${2}/${result}
}
export -f parse

mkdir ${TO_PATH}

find . -type f -name 'W07*.zip' -exec bash -c "parse {} ${TO_PATH}" \;

