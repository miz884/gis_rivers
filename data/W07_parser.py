#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import codecs
import xml.sax
import xml.sax.handler

# output in CSV format.
# 河川コード,河川名,min_lng,min_lat,max_lng,max_lat

sys.stdout = codecs.getwriter('utf_8')(sys.stdout)

class SaxHandler(xml.sax.handler.ContentHandler):
  def __init__(self):
    self.items = [0] * 6
    self.itemIndex = -1
    self.text = ''

  def startElement(self, name, attrs):
    if name == 'Placemark':
      self.items = [0] * 6
      self.itemIndex = -1
      self.text = ''
      return
    if name =='SimpleData' and attrs.getValue('name') == 'W07_003':
      self.itemIndex = 0
      self.text = ''
      return
    if name =='SimpleData' and attrs.getValue('name') == 'W07_005':
      self.itemIndex = 1
      self.text = ''
      return
    if name =='coordinates':
      self.text = ''
      return

  def endElement(self, name):
    if name == 'Placemark':
      print ','.join(self.items)
      return
    if name =='SimpleData' and self.itemIndex >= 0:
      self.items[self.itemIndex] = self.text
      self.itemIndex = -1
      return
    if name =='coordinates':
      lls = self.text.split()
      (min_lng, min_lat) = lls[0].split(',')
      (max_lng, max_lat) = lls[2].split(',')
      self.items[2] = min_lng
      self.items[3] = min_lat
      self.items[4] = max_lng
      self.items[5] = max_lat
      return
  
  def characters(self, content):
    self.text += content
    return

def main():
  parser = xml.sax.make_parser()
  parser.setContentHandler(SaxHandler())
  parser.setFeature(xml.sax.handler.feature_namespaces, False)
  parser.parse(sys.stdin)
  return
  
if __name__=="__main__":
  main()
