import sys
import unittest
import logging
from mesh_code import *

E = 0.000001
def f_equals(f0, f1):
  return (f0 - f1) < E and (f0 - f1) > -E
    

class TestMesh(unittest.TestCase):


  def test_meshcodeToSWNE(self):
    result = meshcodeToSWNE(53394547)

    self.assertEquals(result[0], 35.7000)
    self.assertEquals(result[1], 139.7125)

    # the height of rect should be 30"
    self.assertTrue(f_equals(result[2] - result[0], 30.0 / 60.0 / 60.0))

    # the width of rect should be 45"
    self.assertTrue(f_equals(result[3] - result[1], 45.0 / 60.0 / 60.0))

    # The NE should be equal to SW of (+1, +1) rect.
    result0 = meshcodeToSWNE(53394547)
    result1 = meshcodeToSWNE(53394558)
    self.assertEquals(result0[2], result1[0])
    self.assertEquals(result0[3], result1[1])


  def test_latLngToMeshcode(self):
    result = latLngToMeshcode(35.70078, 139.71475)
    self.assertEquals(result, 53394547)

    result = latLngToMeshcode(35.69999999999999999999999999, 139.7125)
    self.assertEquals(result, 53394547)

    result = latLngToMeshcode(
      Decimal(357000) / Decimal(10000),
      Decimal(1397125) / Decimal(10000))
    self.assertEquals(result, 53394547)


  def test_refrexive(self):
    code = 53394547
    # code -> latlng -> code
    result0 = meshcodeToSWNE(code)
    result1 = latLngToMeshcode(result0[0], result0[1])
    self.assertEquals(result1, code)

    # code -> latlng -> code -> latlng
    result2 = meshcodeToSWNE(result1)
    self.assertEquals(result0[0], result2[0])
    self.assertEquals(result0[1], result2[1])


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stderr)
    logging.getLogger('mesh_code').setLevel(logging.DEBUG)
    unittest.main(failfast=False)
