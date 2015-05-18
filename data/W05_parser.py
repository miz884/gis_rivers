#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import sys
import re
import codecs

sys.stdout = codecs.getwriter('utf_8')(sys.stdout)

BASE_DIR = '/tmp/kml/'

def main():
  isInPm = False
  buffer = ''
  filename = ''
  for line in sys.stdin:
    buffer += line
    if re.match('.*<Placemark>.*', line):
      isInPm = True
      buffer = line
      continue

    if re.match('.*</Placemark>.*', line):
      isInPm = False
      if not os.path.isfile(filename):
        f = open(filename, 'w')
        f.write('<?xml version="1.0" encoding="utf-8" ?>\n')
        f.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
        f.write('<Document id="root_doc">\n')
        f.write(buffer)
        f.close()
      else:
        f = open(filename, 'a')
        f.write(buffer)
        f.close()
      continue

    if isInPm:
      match = re.match('.*<SimpleData name="W05_002">(\d*)<.*', line)
      if match:
        filename = BASE_DIR + match.group(1) + '.kml'
  
if __name__=="__main__":
  main()

