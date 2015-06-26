#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import sys
import re
import codecs

sys.stdout = codecs.getwriter('utf_8')(sys.stdout)

kml_header = '''
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document id="root_doc">
'''.strip()

curve_header = '''
<Placemark>
  <Style><LineStyle><color>ff0000ff</color></LineStyle><PolyStyle><fill>0</fill></PolyStyle></Style>
  <LineString><coordinates>
'''.strip()

curve_footer = '''
  </coordinates></LineString>
</Placemark>
'''.strip()

kml_footer = '''
</Document></kml>
'''.strip()


def mergeCurves(curves):
  remove_targets = []
  for curve0 in curves:
    head = curve0[0]
    for curve1 in curves:
      if curve1 in remove_targets:
        continue
      if curve0 == curve1:
        continue
      tail = curve1[-1]
      if head == tail:
        curve1.extend(curve0)
        remove_targets.append(curve0)
        break

  return [x for x in curves if x not in remove_targets]


def main():
  curves = []
  curr = []

  for line in sys.stdin:
    line = line.strip()

    if len(line) == 0:
      if len(curr) > 0:
        curves.append(curr)
      curr = []
    else:
      curr.append(','.join(reversed(line.split(r' '))))
  if len(curr) > 0:
      curves.append(curr)

  curves = mergeCurves(curves)

  # output the result
  print kml_header
  for curve in curves:
    print curve_header
    print ' '.join(curve)
    print curve_footer
  print kml_footer

if __name__=="__main__":
  main()

