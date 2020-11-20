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
    # Load an index.
    index_store = MeshIndexStore("result/W07_river_mesh_index")
    index = index_store.load(lv1_code)
    # Verify the input and result from the index.
    pattern = re.compile(r'^(\d\d\d\d\d\d\d\d\d\d),(\d*)$')
    with open("result/W07_river_mesh/%s.csv" % (lv1_code), mode="r") as data_file:
        for line in data_file:
            line = line.strip()
            match = pattern.match(line)
            if match:
                mesh_code = str(match.group(1))
                river_code = str(match.group(2))
                code = index.search_by_modified_mesh_code(mesh_code)
                if river_code != code:
                    print("Mismatch on %s. Expected: %s Actual: %s" % (mesh_code,
                                                                       river_code,
                                                                       code))
    print("Done")

if __name__=="__main__":
  main()


