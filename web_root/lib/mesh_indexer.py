#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pickle
import re

class MeshIndex:
    def __init__(self, lv1_code = None, index=[], data_code_map={}):
        self.lv1_code = lv1_code
        self.index = index
        self.data_code_map = data_code_map
        self.mesh_code_pattern = re.compile(r'^(\d\d\d\d)(\d)(\d)(\d)(\d)(\d)(\d)$')
        self.modified_mesh_code_pattern = re.compile(r'^(\d\d)(\d)(\d)(\d)(\d\d)(\d)(\d)(\d)$')

    def _search_sub(self, arr, local_x, local_y):
        target = MeshIndexer.Mesh._calc_index(local_x, local_y)
        pos = 0
        for i in range(0, len(arr), 2):
            pos += arr[i + 1]
            if target < pos:
                return arr[i]
        return None

    def _search(self, lv1, lv2_x, lv2_y, lv3_x, lv3_y, lv4_x, lv4_y):
        result = None
        if lv1 != self.lv1_code:
            return None
        lv2 = self._search_sub(self.index, lv2_x, lv2_y)
        if not isinstance(lv2, list):
            result = lv2
        else:
            lv3 = self._search_sub(lv2, lv3_x, lv3_y)
            if not isinstance(lv3, list):
                result =  lv3
            else:
                result = self._search_sub(lv3, lv4_x, lv4_y)
        if result in self.data_code_map:
            return self.data_code_map[result]
        else:
            return None

    def search_by_mesh_code(self, mesh_code):
        match = self.mesh_code_pattern.match(str(mesh_code))
        if not match:
            return None
        lv1 = int(match.group(1))
        lv2_x = int(match.group(2))
        lv2_y = int(match.group(3))
        lv3_x = int(match.group(4))
        lv3_y = int(match.group(5))
        lv4_x = int(match.group(6))
        lv4_y = int(match.group(7))
        return self._search(lv1, lv2_x, lv2_y, lv3_x, lv3_y, lv4_x, lv4_y)

    def search_by_modified_mesh_code(self, modified_mesh_code):
        match = self.modified_mesh_code_pattern.match(str(modified_mesh_code))
        if not match:
            return None
        lv1 = int(match.group(1)) * 100
        lv2_x = int(match.group(2))
        lv3_x = int(match.group(3))
        lv4_x = int(match.group(4))
        lv1 += int(match.group(5))
        lv2_y = int(match.group(6))
        lv3_y = int(match.group(7))
        lv4_y = int(match.group(8))
        return self._search(lv1, lv2_x, lv2_y, lv3_x, lv3_y, lv4_x, lv4_y)

class MeshIndexer:
    '''
    Index builder for the mesh.
    '''
    def __init__(self):
        self.lv1_code = None
        self.root = MeshIndexer.Mesh.create_root()
        self.curr_data_id = 0
        self.data_code_map = {}
        self.data_code_map_rev = {}
        self.data_code_map["0"] = 0
        self.data_code_map_rev[0] = "0"
        self.mesh_code_pattern = re.compile(r'^(\d\d\d\d)(\d)(\d)(\d)(\d)(\d)(\d)$')
        self.modified_mesh_code_pattern = re.compile(r'^(\d\d)(\d)(\d)(\d)(\d\d)(\d)(\d)(\d)$')

    class Mesh:
        def __init__(self):
            self.parent = None
            self.children = [None] * 100
            self.data_codes = []

        @classmethod
        def _calc_index(cls, x, y):
            return x * 10 + y

        @classmethod
        def create_root(cls):
            root = MeshIndexer.Mesh()
            root.parent = root
            return root

        def get_or_create_child(self, x, y):
            pos = MeshIndexer.Mesh._calc_index(x, y)
            result = self.children[pos]
            if result is None:
                result = MeshIndexer.Mesh()
                result.parent = self
                self.children[pos] = result
            return result

        def add_data(self, x, y, data_code):
            self.children[MeshIndexer.Mesh._calc_index(x, y)] = data_code
            cur = self
            while (cur.parent != cur):
                if data_code not in cur.data_codes:
                    cur.data_codes.append(data_code)
                cur = cur.parent


    def _get_data_id(self, data_code):
        if data_code in self.data_code_map:
            return self.data_code_map[data_code]
        self.curr_data_id += 1
        data_id = self.curr_data_id
        self.data_code_map[data_code] = data_id
        self.data_code_map_rev[data_id] = data_code
        return data_id

    def _add_data(self, lv1, lv2_x, lv2_y, lv3_x, lv3_y, lv4_x, lv4_y, data_code):
        if self.lv1_code is None:
            self.lv1_code = lv1
        elif self.lv1_code != lv1:
            return None
        data_id = self._get_data_id(data_code)
        lv2 = self.root.get_or_create_child(lv2_x, lv2_y)
        lv3 = lv2.get_or_create_child(lv3_x, lv3_y)
        lv3.add_data(lv4_x, lv4_y, data_id)

    def add_data_by_mesh_code(self, mesh_code, data_code):
        match = self.mesh_code_pattern.match(mesh_code)
        if not match:
            return None
        lv1 = int(match.group(1))
        lv2_x = int(match.group(2))
        lv2_y = int(match.group(3))
        lv3_x = int(match.group(4))
        lv3_y = int(match.group(5))
        lv4_x = int(match.group(6))
        lv4_y = int(match.group(7))
        self._add_data(lv1, lv2_x, lv2_y, lv3_x, lv3_y, lv4_x, lv4_y, data_code)

    def add_data_by_modified_mesh_code(self, modified_mesh_code, data_code):
        match = self.modified_mesh_code_pattern.match(modified_mesh_code)
        if not match:
            return None
        lv1 = int(match.group(1)) * 100
        lv2_x = int(match.group(2))
        lv3_x = int(match.group(3))
        lv4_x = int(match.group(4))
        lv1 += int(match.group(5))
        lv2_y = int(match.group(6))
        lv3_y = int(match.group(7))
        lv4_y = int(match.group(8))
        self._add_data(lv1, lv2_x, lv2_y, lv3_x, lv3_y, lv4_x, lv4_y, data_code)


    def build_index(self):
        def compress_recursively(node):
            '''
            Compress the index by removing redundancy in the tree.
            If a node covers only a sngle code, the 10x10 area will
            be compressed to a single  code.
            '''
            if node is None:
                return "0"
            if not isinstance(node, MeshIndexer.Mesh):
                return node
            if len(node.data_codes) == 1:
                return node.data_codes[0]
            for i in range(100):
                node.children[i] = compress_recursively(node.children[i])
            return node

        def to_array_recursively(node):
            '''
            Covert the tree of Mesh into an array representation.
            It will lost the bi-directional pointer for parents and
            children. Instead, it will be compact.
            Example:
              # lv2, about 100km x 100km
              [
                # lv3, about 10km x 10km
                [
                  # lv4, about 1km x 1km
                  [1, ... , 2]
                  2,
                  [3, 2, ... , 3]
                  ...
                  [100, ... , 101]
                ]
                ...
                [
                  [ ... ]
                  ...
                  [ ... ]
                ]
              ]
            '''
            if node is None:
                return 0
            if not isinstance(node, MeshIndexer.Mesh):
                return node
            result = []
            for i in range(100):
                result.append(to_array_recursively(node.children[i]))
            return result

        def runlength_recursively(node):
            '''
            Compress the index by run-length algorithm.
            The run-length will be counted in the 100 cells in a Mesh.
            The border of Mesh will break a sequence of data IDs.
            The result will be a series of pairs of <data_id> and <count>.
            Example:
              # lv2, about 100km x 100km
              [
                # lv3, about 10km x 10km
                [
                  # lv4, about 1km x 1km
                  [1, 80, 2, 20] # 
                  2, 1,
                  [3, 1, 2, 90, 3, 8]
                  ...
                  [100, 99, 101, 1]
                ]
                ...
                [
                  [ ... ]
                  ...
                  [ ... ]
                ]
              ]
            '''
            result = []
            prev = None
            curr = None
            count = 0
            for i in range(len(node)):
                curr = node[i]
                if isinstance(curr, list):
                    if count > 0:
                        result.append(prev)
                        result.append(count)
                    result.append(runlength_recursively(curr))
                    result.append(1)
                    prev = None
                    count = 0
                else:
                    if prev is None:
                        prev = curr
                        count = 1
                    elif curr == prev:
                        count += 1
                    else:
                        result.append(prev)
                        result.append(count)
                        prev = curr
                        count = 1
            if count > 0:
                result.append(curr)
                result.append(count)
            return result

        index = compress_recursively(self.root)
        index = to_array_recursively(index)
        index = runlength_recursively(index)
        return MeshIndex(lv1_code = self.lv1_code,
                         index=index,
                         data_code_map=self.data_code_map_rev)


class MeshIndexStore:
    def __init__(self, target_dir):
        self.target_dir = target_dir

    def _get_path(self, lv1_code):
        return "%s/%s.dump" % (self.target_dir, lv1_code)

    def save(self, lv1_code, index):
        path = self._get_path(lv1_code)
        with open(path, mode='wb') as f:
            pickle.dump(index, f)

    def load(self, lv1_code):
        path = self._get_path(lv1_code)
        with open(path, mode='rb') as f:
            index = pickle.load(f)
            return index


class MeshIndexFacade:
    def __init__(self, target_dir):
        self.index_store = MeshIndexStore(target_dir)
        self.mesh_code_pattern = re.compile(r'^(\d\d\d\d)(\d)(\d)(\d)(\d)(\d)(\d)$')
        self.modified_mesh_code_pattern = re.compile(r'^(\d\d)(\d)(\d)(\d)(\d\d)(\d)(\d)(\d)$')

    def search_by_mesh_code(self, mesh_code):
        match = self.mesh_code_pattern.match(str(mesh_code))
        if not match:
            return None
        lv1 = int(match.group(1))
        lv2_x = int(match.group(2))
        lv2_y = int(match.group(3))
        lv3_x = int(match.group(4))
        lv3_y = int(match.group(5))
        lv4_x = int(match.group(6))
        lv4_y = int(match.group(7))
        index = self.index_store.load(lv1)
        return index._search(lv1, lv2_x, lv2_y, lv3_x, lv3_y, lv4_x, lv4_y)

    def search_by_modified_mesh_code(self, modified_mesh_code):
        match = self.modified_mesh_code_pattern.match(str(modified_mesh_code))
        if not match:
            return None
        lv1 = int(match.group(1)) * 100
        lv2_x = int(match.group(2))
        lv3_x = int(match.group(3))
        lv4_x = int(match.group(4))
        lv1 += int(match.group(5))
        lv2_y = int(match.group(6))
        lv3_y = int(match.group(7))
        lv4_y = int(match.group(8))
        index = self.index_store.load(lv1)
        return index._search(lv1, lv2_x, lv2_y, lv3_x, lv3_y, lv4_x, lv4_y)


