#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re

def main():
    # Build an index.
    mesh_cache = {}
    pattern = re.compile(r'^(\d\d\d\d\d\d\d\d\d\d),(\d\d\d\d\d\d)(\d\d\d\d)$')
    with open("result/W07_river_mesh/all.csv", mode="r") as data_file:
        for line in data_file:
            line = line.strip()
            match = pattern.match(line)
            if match:
                modified_mesh_code = str(match.group(1))
                water_system_code = str(match.group(2))
                l = None
                if water_system_code in mesh_cache:
                    l = mesh_cache[water_system_code]
                else:
                    l = []
                    mesh_cache[water_system_code] = l
                l.append(modified_mesh_code)

    code_pattern = re.compile(r'^(\d\d)\d*$')
    for water_system_code in mesh_cache.keys():
        print("Processing %s." % water_system_code)
        mesh_codes = mesh_cache[water_system_code]
        mesh_codes.sort()
        match = code_pattern.match(water_system_code)
        pref_code = match.group(1)
        dir_path = "result/water_system_mesh_list/%s" % (pref_code)
        os.makedirs(dir_path, exist_ok=True)
        file_path = "result/water_system_mesh_list/%s/%s" % (pref_code, water_system_code)
        with open(file_path, mode="w") as f:
            f.write('\n'.join(mesh_codes))

if __name__=="__main__":
  main()

