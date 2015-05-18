#!/bin/sh

function shp2kml {
  SHP=$1
  KML=${SHP%.*}.kml
  echo ogr2ogr -f KML ${KML} ${SHP}
}
export -f shp2kml

find . -name '*.shp' -exec bash -c "shp2kml {}" \;
