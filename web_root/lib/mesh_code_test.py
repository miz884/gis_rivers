import sys
import unittest
import logging
from mesh_code import *

E = 0.000001
def f_equals(f0, f1):
  return (f0 - f1) < E and (f0 - f1) > -E


class TestMesh(unittest.TestCase):

  def test_meshCodeToSWNE(self):
    result = meshCodeToSWNE(5339454701)

    self.assertEquals(result[0], 35.7000)
    self.assertEquals(result[1], 139.71375)

    # the height of rect should be 3"
    self.assertTrue(f_equals(result[2] - result[0], 3.0 / 60.0 / 60.0))

    # the width of rect should be 4.5"
    self.assertTrue(f_equals(result[3] - result[1], 4.5 / 60.0 / 60.0))

    # check (+1, 0) rect
    result0 = meshCodeToSWNE(5339454701)
    result1 = meshCodeToSWNE(5339454711)
    self.assertEquals(result0[1], result1[1]) # w0 == w1
    self.assertEquals(result0[3], result1[3]) # e0 == e1
    self.assertEquals(result0[2], result1[0]) # n0 == s1

    # check (0, +1) rect
    result0 = meshCodeToSWNE(5339454701)
    result1 = meshCodeToSWNE(5339454702)
    self.assertEquals(result0[0], result1[0]) # s0 == s1
    self.assertEquals(result0[2], result1[2]) # n0 == n1
    self.assertEquals(result0[3], result1[1]) # e0 == w1

    # The NE should be equal to SW of (+1, +1) rect.
    result0 = meshCodeToSWNE(5339454701)
    result1 = meshCodeToSWNE(5339454712)
    self.assertEquals(result0[2], result1[0]) # n0 == s1
    self.assertEquals(result0[3], result1[1]) # e0 == w1


  def test_latLngToMeshCode(self):
    result = latLngToMeshCode(35.70078, 139.71475)
    self.assertEquals(result, 5339454701)

    result = latLngToMeshCode(35.69999999999999999999999999, 139.7125)
    self.assertEquals(result, 5339454700)

    result = latLngToMeshCode(
      Decimal(357000) / Decimal(10000),
      Decimal(13971475) / Decimal(100000))
    self.assertEquals(result, 5339454701)


  def test_refrexive(self):
    code = 5339454701
    # code -> latlng -> code
    result0 = meshCodeToSWNE(code)
    result1 = latLngToMeshCode(result0[0], result0[1])
    self.assertEquals(result1, code)

    # code -> latlng -> code -> latlng
    result2 = meshCodeToSWNE(result1)
    self.assertEquals(result0[0], result2[0])
    self.assertEquals(result0[1], result2[1])


  def test_modifiedMeshCodeToMeshCode(self):
    result = modifiedMeshCodeToMeshCode(1234567890)
    self.assertEquals(result, 1267384950)

    result = modifiedMeshCodeToMeshCode(5344039571)
    self.assertEquals(result, 5339454701)


  def test_meshCodeToModifiedMeshCode(self):
    result = meshCodeToModifiedMeshCode(1234567890)
    self.assertEquals(result, 1257934680)

    result = meshCodeToModifiedMeshCode(5339454701)
    self.assertEquals(result, 5344039571)


  def test_modifiedMeshCodeToSWNE(self):
    result = modifiedMeshCodeToSWNE(5344039571)
    self.assertEquals(result[0], 35.7000)
    self.assertEquals(result[1], 139.71375)


  def test_latLngToModifiedMeshCode(self):
    result = latLngToModifiedMeshCode(35.70078, 139.71375)
    self.assertEquals(result, 5344039571)


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stderr)
    logging.getLogger('mesh_code').setLevel(logging.DEBUG)
    unittest.main(failfast=False)
