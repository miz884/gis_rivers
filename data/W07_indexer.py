#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), '../web_root/lib'))

from mesh_indexer import *

def main():
    if len(sys.argv) != 2:
        print("Please specify level 1 mesh code.")
        return
    lv1_code = sys.argv[1]
    # Build an index.
    indexer = MeshIndexer()
    pattern = re.compile(r'^(\d\d\d\d\d\d\d\d\d\d),(\d*)$')
    with open("result/W07_river_mesh/%s.csv" % (lv1_code), mode="r") as data_file:
        for line in data_file:
            line = line.strip()
            match = pattern.match(line)
            if match:
                modified_mesh_code = str(match.group(1))
                river_code = str(match.group(2))
                indexer.add_data_by_modified_mesh_code(modified_mesh_code, river_code)

    index = indexer.build_index()
    index_store = MeshIndexStore("result/W07_river_mesh_index")
    index_store.save(lv1_code, index)

if __name__=="__main__":
  main()

