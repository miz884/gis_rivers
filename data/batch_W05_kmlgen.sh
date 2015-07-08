#!/bin/sh

FROM_PATH=./result/W05_river_path_data/
TO_PATH=./result/W05_river_path_kmz/

function kmzgen {
  echo "processing ${1}..."
  target=$(basename ${1} | sed -e 's/data/kmz/')
  cat ${1} | python ./W05_kmlgen.py > /tmp/doc.kml
  zip -j ${2}/${target} /tmp/doc.kml
}
export -f kmzgen

mkdir ${TO_PATH}

find ${FROM_PATH} -name '*.data' -exec bash -c "kmzgen {} ${TO_PATH}" \;


