#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import sys
import re
import codecs

sys.stdout = codecs.getwriter('utf_8')(sys.stdout)

BASE_DIR = '/tmp/W05_river_path/'


def main():
  curves = {}
  streams = {}
  curr_curve_id = None
  curr_curve_ref = None

  for line in sys.stdin:
    line = line.strip()
    '''
    Sample curve:
    -----------------------------------
    <gml:Curve gml:id="c-1">
        <gml:segments>
                <gml:LineStringSegment>
                        <gml:posList>
    35.88983818 139.01777656
    ...
    35.88956978 139.01798399
                        </gml:posList>
                </gml:LineStringSegment>
        </gml:segments>
    </gml:Curve>
    -----------------------------------
    '''
    match = re.match(r'<gml:Curve gml:id="(c-\d*)">', line)
    if match:
      curr_curve_id = match.group(1)
      if not curr_curve_id in curves:
        curves[curr_curve_id] = []

    match = re.match(r'^\d*\.\d* \d*\.\d*$', line)
    if match and curr_curve_id:
      curves[curr_curve_id].append(line)

    match = re.match(r'</gml:Curve>', line)
    if match:
      curr_curve_id = None

    '''
    Sample stream:
    -----------------------------------
    <ksj:Stream gml:id="r-1">
        <ksj:waterSystemCode codeSpace="WaterSystemTypeCode.xml">830305</ksj:waterSystemCode>
        <ksj:location xlink:href="#c-1"/>
        <ksj:riverCode codeSpace="RiverTypeCode.xml">8303050000</ksj:riverCode>
        <ksj:sectionType>0</ksj:sectionType>
        <ksj:riverName>小川谷</ksj:riverName>
        <ksj:originalDataType>3</ksj:originalDataType>
        <ksj:flowDirection>1</ksj:flowDirection>
        <ksj:startRiverNode xlink:href="#gb03_1300005"/>
        <ksj:endRiverNode xlink:href="#gb03_1300079"/>
        <ksj:startStreamNode xlink:href="#gb03_1300005"/>
        <ksj:endStreamNode xlink:href="#gb03_1300006"/>
    </ksj:Stream>
    -----------------------------------
    '''
    match = re.match(r'<ksj:location xlink:href="#(c-\d*)"/>', line)
    if match:
      curr_curve_ref = match.group(1)

    match = re.match(r'<ksj:riverCode codeSpace="RiverTypeCode.xml">(\d*)</ksj:riverCode>', line)
    if match and curr_curve_ref:
      river_code = match.group(1)
      if not river_code in streams:
        streams[river_code] = []
      streams[river_code].append(curves[curr_curve_ref])

    match = re.match(r'</ksj:Stream>', line)
    if match:
      curr_curve_ref = None

  for code, paths in streams.iteritems():
    filename = BASE_DIR + code + '.data'
    f = None
    if not os.path.isfile(filename):
      f = open(filename, 'w')
    else:
      f = open(filename, 'a')

    for path in paths:
      f.write('\n')
      for point in path:
        f.write(point + '\n')
    f.close()

if __name__=="__main__":
  main()

