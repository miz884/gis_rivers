import sys
import unittest
import logging
from mesh import *

log = logging.getLogger('mesh')


class TestMesh(unittest.TestCase):

  def test_get(self):
    self.assertFalse(Mesh(1) is Mesh(1))
    self.assertTrue(Mesh.get(1) is Mesh.get(1))

  def test_eq(self):
    self.assertTrue(Mesh(1) == Mesh(1))
    self.assertFalse(Mesh(1) == Mesh(2))

  def test_ne(self):
    self.assertTrue(Mesh(1) != Mesh(2))
    self.assertFalse(Mesh(1) != Mesh(1))

  def test_gt(self):
    self.assertTrue(Mesh(1) < Mesh(2))
    self.assertFalse(Mesh(1) < Mesh(1))

  def test_lt(self):
    self.assertTrue(Mesh(2) > Mesh(1))
    self.assertFalse(Mesh(1) > Mesh(1))

  def test_ge(self):
    self.assertTrue(Mesh(1) <= Mesh(1))
    self.assertTrue(Mesh(1) <= Mesh(2))
    self.assertFalse(Mesh(2) <= Mesh(1))

  def test_le(self):
    self.assertTrue(Mesh(1) >= Mesh(1))
    self.assertTrue(Mesh(2) >= Mesh(1))
    self.assertFalse(Mesh(1) >= Mesh(2))

  def test_max(self):
    self.assertEqual(Mesh.get(5), max([Mesh.get(3),
                                       Mesh.get(2),
                                       Mesh.get(5),
                                       Mesh.get(4),
                                       Mesh.get(1)]))

  def test_min(self):
    self.assertEqual(Mesh.get(1), min([Mesh.get(3),
                                       Mesh.get(2),
                                       Mesh.get(5),
                                       Mesh.get(4),
                                       Mesh.get(1)]))

  def test_list(self):
    self.assertTrue(Mesh.get(1) in [Mesh.get(3),
                                    Mesh.get(2),
                                    Mesh.get(5),
                                    Mesh.get(4),
                                    Mesh.get(1)])
    self.assertTrue(Mesh.get(1) not in [Mesh.get(3),
                                        Mesh.get(2),
                                        Mesh.get(5),
                                        Mesh.get(4)])

  def test_south(self):
    mesh = Mesh.get(1000100002)
    target = Mesh.get(1000000002)
    self.assertEqual(target,  mesh.south())

  def test_north(self):
    mesh = Mesh.get(1000100002)
    target = Mesh.get(1000200002)
    self.assertEqual(target, mesh.north())

  def test_west(self):
    mesh = Mesh.get(1000100002)
    target = Mesh.get(1000100001)
    self.assertEqual(target, mesh.west())

  def test_east(self):
    mesh = Mesh.get(1000100002)
    target = Mesh.get(1000100003)
    self.assertEqual(target, mesh.east())



class TestMeshMerger(unittest.TestCase):

  def test_calcNextCornerCodes(self):
    m0 = Mesh.get(1000100000)
    m1 = Mesh.get(1000100001)
    m2 = Mesh.get(1000000001)
    m3 = Mesh.get(1000000000)
    corner = m1

    hash = {}
    with self.assertRaises(Exception) as cm:
        MeshMerger._calcNextCornerCodes(corner, hash)

    hash = {}
    hash[m0.code] = m0
    result = MeshMerger._calcNextCornerCodes(corner, hash)
    self.assertEqual(1, len(result))
    self.assertEqual(m1.west(), result[0])

    hash = {}
    hash[m1.code] = m1
    result = MeshMerger._calcNextCornerCodes(corner, hash)
    self.assertEqual(1, len(result))
    self.assertEqual(m1.north(), result[0])

    hash = {}
    hash[m0.code] = m0
    hash[m1.code] = m1
    result = MeshMerger._calcNextCornerCodes(corner, hash)
    self.assertEqual(1, len(result))
    self.assertEqual(m1.west(), result[0])

    hash = {}
    hash[m2.code] = m2
    result = MeshMerger._calcNextCornerCodes(corner, hash)
    self.assertEqual(1, len(result))
    self.assertEqual(m1.east(), result[0])

    hash = {}
    hash[m0.code] = m0
    hash[m2.code] = m2
    result = MeshMerger._calcNextCornerCodes(corner, hash)
    self.assertEqual(2, len(result))
    self.assertTrue(m1.east() in result)
    self.assertTrue(m1.west() in result)

    hash = {}
    hash[m1.code] = m1
    hash[m2.code] = m2
    result = MeshMerger._calcNextCornerCodes(corner, hash)
    self.assertEqual(1, len(result))
    self.assertEqual(m1.north(), result[0])

    hash = {}
    hash[m0.code] = m0
    hash[m1.code] = m1
    hash[m2.code] = m2
    result = MeshMerger._calcNextCornerCodes(corner, hash)
    self.assertEqual(1, len(result))
    self.assertEqual(m1.west(), result[0])

    hash = {}
    hash[m3.code] = m3
    result = MeshMerger._calcNextCornerCodes(corner, hash)
    self.assertEqual(1, len(result))
    self.assertEqual(m1.south(), result[0])

    hash = {}
    hash[m0.code] = m0
    hash[m3.code] = m3
    result = MeshMerger._calcNextCornerCodes(corner, hash)
    self.assertEqual(1, len(result))
    self.assertEqual(m1.south(), result[0])

    hash = {}
    hash[m1.code] = m1
    hash[m3.code] = m3
    result = MeshMerger._calcNextCornerCodes(corner, hash)
    self.assertEqual(2, len(result))
    self.assertTrue(m1.north() in result)
    self.assertTrue(m1.south() in result)

    hash = {}
    hash[m0.code] = m0
    hash[m1.code] = m1
    hash[m3.code] = m3
    result = MeshMerger._calcNextCornerCodes(corner, hash)
    self.assertEqual(1, len(result))
    self.assertEqual(m1.south(), result[0])

    hash = {}
    hash[m2.code] = m2
    hash[m3.code] = m3
    result = MeshMerger._calcNextCornerCodes(corner, hash)
    self.assertEqual(1, len(result))
    self.assertEqual(m1.east(), result[0])

    hash = {}
    hash[m0.code] = m0
    hash[m2.code] = m2
    hash[m3.code] = m3
    result = MeshMerger._calcNextCornerCodes(corner, hash)
    self.assertEqual(1, len(result))
    self.assertEqual(m1.east(), result[0])

    hash = {}
    hash[m1.code] = m1
    hash[m2.code] = m2
    hash[m3.code] = m3
    result = MeshMerger._calcNextCornerCodes(corner, hash)
    self.assertEqual(1, len(result))
    self.assertEqual(m1.north(), result[0])

    hash = {}
    hash[m0.code] = m0
    hash[m1.code] = m1
    hash[m2.code] = m2
    hash[m3.code] = m3
    with self.assertRaises(Exception) as cm:
        MeshMerger._calcNextCornerCodes(corner, hash)

  def test_merge(self):
    result = MeshMerger.merge([1])
    self.assertEqual([[1, 100001, 100002, 2, 1]], result)

    result = MeshMerger.merge([1, 2])
    self.assertEqual([[1, 100001, 100002, 100003, 3, 2, 1]], result)

    result = MeshMerger.merge([1, 2, 3])
    self.assertEqual([[1, 100001, 100002, 100003, 100004, 4,  3, 2, 1]], result)

    result = MeshMerger.merge([1, 3])
    self.assertEqual([[1, 100001, 100002, 2, 1], [3, 100003, 100004, 4, 3]], result)

    result = MeshMerger.merge([1, 100001])
    self.assertEqual([[1, 100001, 200001, 200002, 100002, 2, 1]], result)

    result = MeshMerger.merge([1, 2, 100001])
    self.assertEqual([[1, 100001, 200001, 200002, 100002, 100003, 3, 2, 1]], result)

    result = MeshMerger.merge([1, 2, 100001, 100002])
    self.assertEqual([[1, 100001, 200001, 200002, 200003, 100003, 3, 2, 1]], result)

    result = MeshMerger.merge([1, 3, 100001, 100002, 100003])
    self.assertEqual([[1, 100001, 200001, 200002, 200003, 200004,
                       100004, 4, 3, 100003, 100002, 2, 1]], result)


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stderr)
    logging.getLogger('mesh').setLevel(logging.DEBUG)
    unittest.main(failfast=False)

