#!/bin/sh

TARGET_PATH=./result/W05_river_path_kmz/
DIRS="01 02 03 04 05 06 07 08 12 13 14 15 16 17 18 19 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 81 82 83 84 85 86 87 88 89"

for D in ${DIRS}; do
  mkdir ${TARGET_PATH}${D}
  find ${TARGET_PATH} -type f -name "${D}*.kmz" -exec mv "{}" ${TARGET_PATH}${D}/ \;
done

