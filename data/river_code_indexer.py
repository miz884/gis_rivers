#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pickle
import re

def main():
    pattern = re.compile(r'^(\d*),(.*)$')
    index = {}
    with open("river_code.csv", mode="r") as data_file:
        for line in data_file:
            line = line.strip()
            match = pattern.match(line)
            if match:
                river_code = str(match.group(1))
                river_name = str(match.group(2))
                index[river_code] = river_name

    with open("river_code_index.dump", mode="wb") as index_file:
        pickle.dump(index, index_file)

if __name__=="__main__":
  main()

