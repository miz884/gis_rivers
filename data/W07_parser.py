#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import sys
import re
import codecs

sys.stdout = codecs.getwriter('utf_8')(sys.stdout)
sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), '../web_root/lib'))

from mesh_code import *

def main():

  print('modified_mesh_code,river_code')
  pattern = re.compile(r'^(\d*),(\d*),(\d*),([^,]*),([^,]*),(\d*)$')
  for line in sys.stdin:
    line = line.strip()
    '''
    Data format:
    -----------------------------------
    <ksj:ValleyMesh gml:id="fi_1">
        <gml:domainSet xlink:href="#grid"/>
        <gml:rangeSet>
                <gml:DataBlock>
                        <gml:rangeParameters xlink:href="#recordType"/>
                        <gml:tupleList>
    5339000000,140019,1400190001,酒匂川,鮎沢川,42
    5339000001,140019,1400190001,酒匂川,鮎沢川,41
    ...
    5339000098,140019,1400190000,酒匂川,畑沢,39
    5339000099,140019,1400190000,酒匂川,畑沢,39
                        </gml:tupleList>
                </gml:DataBlock>
        </gml:rangeSet>
        <gml:coverageFunction>
                <gml:GridFunction>
                        <gml:sequenceRule axisOrder="+1 +2">Linear</gml:sequenceRule>
                        <gml:startPoint>0 0</gml:startPoint>
                </gml:GridFunction>
        </gml:coverageFunction>
        <ksj:tertiaryMeshCode>53390000</ksj:tertiaryMeshCode>
    </ksj:ValleyMesh>
    -----------------------------------
    '''
    match = pattern.match(line)
    if match:
      mesh_code = match.group(1)
      river_code = match.group(3)
      modified_mesh_code = meshCodeToModifiedMeshCode(mesh_code)
      print('%d,%s' % (modified_mesh_code, river_code))

if __name__=="__main__":
  main()

