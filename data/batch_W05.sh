#!/bin/sh

function parse {
  echo "parsing ${1}..."
  cat ${1} | python W05_parser.py
}
export -f parse

function finalize {
  echo '</Document></kml>' >> ${1}
}
export -f finalize

if [ -d /tmp/kml ]; then
  echo "/tmp/kml already exists."  >&2
  exit
fi

mkdir /tmp/kml
find . -name '*_Stream.kml' -exec bash -c "parse {}" \;

echo "finalizing..."
find /tmp/kml -name '*.kml' -exec bash -c "finalize {}" \;

