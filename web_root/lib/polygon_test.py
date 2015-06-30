import sys
import unittest
import logging
from polygon import *

class TestRect(unittest.TestCase):

  def test_connectHorizontally(self):
    r = Rect(0, 0, 1, 1)
    r1 = Rect(0, 1, 1, 2)
    result = r.connectHorizontally(r1)
    self.assertTrue(result)
    self.assertEquals(r.south, 0)
    self.assertEquals(r.west, 0)
    self.assertEquals(r.north, 1)
    self.assertEquals(r.east, 2)

    r = Rect(0, 0, 1, 1)
    r1 = Rect(0, 2, 1, 3)
    result = r.connectHorizontally(r1)
    self.assertFalse(result)
    self.assertEquals(r.south, 0)
    self.assertEquals(r.west, 0)
    self.assertEquals(r.north, 1)
    self.assertEquals(r.east, 1)

  def test_toPolygonArray(self):
    r = Rect(0, 1, 2, 3)
    result = r.toPolygonArray()
    self.assertListEqual(result, [[0, 1], [0, 3], [2, 3],
                                  [2, 1], [0, 1]])


class TestPathPoint(unittest.TestCase):

  def test_construct(self):
    pp = PathPoint(0, 1)
    self.assertEquals(pp.lat, 0)
    self.assertEquals(pp.lng, 1)

  def test_connectNext(self):
    pp = PathPoint(0, 0)
    pp1 = PathPoint(1, 1)
    pp.connectNext(pp1)
    self.assertEquals(pp.next, pp1)
    self.assertIsNone(pp.prev)
    self.assertEquals(pp1.prev, pp)
    self.assertIsNone(pp1.next)

  def test_connectPrev(self):
    pp = PathPoint(0, 0)
    pp1 = PathPoint(1, 1)
    pp.connectPrev(pp1)
    self.assertIsNone(pp.next)
    self.assertEquals(pp.prev, pp1)
    self.assertIsNone(pp1.prev)
    self.assertEquals(pp1.next, pp)

  def test_toCoord(self):
    pp = PathPoint(0, 1)
    result = pp.toCoord()
    self.assertEquals(result[0], 0)
    self.assertEquals(result[1], 1)


class TestPath(unittest.TestCase):

  def test_createPathFromRect(self):
    r = Rect(0, 1, 2, 3)
    p = Path.createPathFromRect(r)
    # north west
    self.assertEquals(p.head.lat, 2)
    self.assertEquals(p.head.lng, 1)
    # south west
    self.assertEquals(p.head.prev.lat, 0)
    self.assertEquals(p.head.prev.lng, 1)
    # south east
    self.assertEquals(p.head.prev.prev.lat, 0)
    self.assertEquals(p.head.prev.prev.lng, 3)
    # north east
    self.assertEquals(p.head.prev.prev.prev.lat, 2)
    self.assertEquals(p.head.prev.prev.prev.lng, 3)

    self.assertEquals(p.head.prev.prev.prev, p.tail)

  def test_appendHead(self):
    p = Path()
    p1 = PathPoint(0, 1)
    p.appendHead(p1)
    self.assertEquals(p.head, p1)
    self.assertEquals(p.tail, p1)
    p2 = PathPoint(2, 3)
    p.appendHead(p2)
    self.assertEquals(p.head, p2)
    self.assertEquals(p.tail, p1)
    self.assertIsNone(p2.next)
    self.assertEquals(p2.prev, p1)
    self.assertEquals(p1.next, p2)
    self.assertIsNone(p1.prev)
    
  def test_appendTail(self):
    p = Path()
    p1 = PathPoint(0, 1)
    p.appendTail(p1)
    self.assertEquals(p.head, p1)
    self.assertEquals(p.tail, p1)
    p2 = PathPoint(2, 3)
    p.appendTail(p2)
    self.assertEquals(p.head, p1)
    self.assertEquals(p.tail, p2)
    self.assertEquals(p2.next, p1)
    self.assertIsNone(p2.prev)
    self.assertIsNone(p1.next)
    self.assertEquals(p1.prev, p2)

  def test_isOuterCircle(self):
    return

  def test_isInnerCircle(self):
    return


class TestPoly(unittest.TestCase):

  def test_createPolyFromRect(self):
    r = Rect(0, 1, 2, 3)
    p = Poly.createPolyFromRect(r)
    self.assertEquals(p.north, 2)
    self.assertEquals(p.west, 1)
    self.assertEquals(p.east, 3)

  def test_isTouching(self):
    r = Rect(0, 0, 1, 1)
    p = Poly.createPolyFromRect(r)

    # Vertically separated.
    target = Poly.createPolyFromRect(Rect(2, 0, 3, 1))
    self.assertFalse(p.isTouching(target))

    # 0 ---- 1
    # 0 ---- 1
    target = Poly.createPolyFromRect(Rect(1, 0, 2, 1))
    self.assertTrue(p.isTouching(target))

    #                0 ---- 1
    # -1 ---- -0.5
    target = Poly.createPolyFromRect(Rect(1, -1, 2, -0.5))
    self.assertFalse(p.isTouching(target))

    #        0 ---- 1
    # -0.5 ---- 0.5
    target = Poly.createPolyFromRect(Rect(1, -0.5, 2, 0.5))
    self.assertTrue(p.isTouching(target))

    # 0 ---- 1
    #   0.5 ---- 1.5
    target = Poly.createPolyFromRect(Rect(1, 0.5, 2, 1.5))
    self.assertTrue(p.isTouching(target))

    # 0 ---- 1
    #            1.5 ---- 2.5
    target = Poly.createPolyFromRect(Rect(1, 1.5, 2, 2.5))
    self.assertFalse(p.isTouching(target))

    #      0 ---- 1
    # -0.5 -------- 1.5
    target = Poly.createPolyFromRect(Rect(1, -0.5, 2, 1.5))
    self.assertTrue(p.isTouching(target))

    #   0 ---- 1
    # 0.25 -- 0.75
    target = Poly.createPolyFromRect(Rect(1, 0.25, 2, 0.75))
    self.assertTrue(p.isTouching(target))

  def test_addPolys(self):
    p = Poly.createPolyFromRect(Rect(0, 0, 1, 1))
    a = p.toPolygonArray()
    p.addPolys([])
    self.assertListEqual(p.toPolygonArray(), a)

    p = Poly.createPolyFromRect(Rect(0, 0, 1, 1))
    target = Poly.createPolyFromRect(Rect(1, 0, 2, 1))
    self.assertTrue(p.isTouching(target))
    p.addPolys([target])
    self.assertListEqual(target.toPolygonArray(),
                         [[2, 0], [1, 0], [0, 0],
                          [0, 1], [1, 1], [2, 1]])

    p = Poly.createPolyFromRect(Rect(0, 0, 1, 1))
    target = Poly.createPolyFromRect(Rect(1, 0, 2, 1))
    p.addPolys([target])
    target2 = Poly.createPolyFromRect(Rect(2, 0, 3, 1))
    target.addPolys([target2])
    self.assertListEqual(target2.toPolygonArray(),
                         [[3, 0], [2, 0], [1, 0], [0, 0],
                          [0, 1], [1, 1], [2, 1], [3, 1]])

    p = Poly.createPolyFromRect(Rect(0, 0, 1, 2))
    target = Poly.createPolyFromRect(Rect(1, -1, 2, 1))
    p.addPolys([target])
    self.assertListEqual(target.toPolygonArray(),
                         [[2, -1], [1, -1], [1, 0], [0, 0], [0, 2],
                          [1, 2], [1, 1], [2, 1]])

    p = Poly.createPolyFromRect(Rect(0, 1, 1, 4))
    target = Poly.createPolyFromRect(Rect(1, 0, 2, 2))
    target2 = Poly.createPolyFromRect(Rect(1, 3, 2, 5))
    p.addPolys([target, target2])
    self.assertListEqual(target.toPolygonArray(),
                         [[2, 0], [1, 0], [1, 1], [0, 1], [0, 4],
                          [1, 4], [1, 5], [2, 5]])
    self.assertListEqual(target2.toPolygonArray(),
                         [[2, 3], [1, 3], [1, 2], [2, 2]])

    p = Poly.createPolyFromRect(Rect(0, 1, 1, 4))
    target = Poly.createPolyFromRect(Rect(1, 0, 2, 2))
    target2 = Poly.createPolyFromRect(Rect(1, 3, 2, 5))
    p.addPolys([target, target2])
    target3 = Poly.createPolyFromRect(Rect(2, 4, 3, 6))
    target.addPolys([target3])
    target2.addPolys([target3])
    self.assertListEqual(target.toPolygonArray(),
                         [[2, 0], [1, 0], [1, 1], [0, 1], [0, 4],
                          [1, 4], [1, 5], [2, 5], [2, 6], [3, 6]])
    self.assertListEqual(target3.toPolygonArray(),
                         [[3, 4], [2, 4], [2, 3], [1, 3], [1, 2], [2, 2]])


  def test_toPolygonArray(self):
    r = Rect(0, 1, 2, 3)
    p = Poly.createPolyFromRect(r)
    result = p.toPolygonArray()
    self.assertListEqual(result, [[2, 1], [0, 1], [0, 3], [2, 3]])

  def test_finalize(self):
    r = Rect(0, 1, 2, 3)
    p = Poly.createPolyFromRect(r)
    p.finalize()
    result = p.toPolygonArray()
    self.assertListEqual(result, [[2, 1], [0, 1], [0, 3], [2, 3], [2, 1]])


class TestPolyMerger(unittest.TestCase):

  def test_mergeSquare(self):
    return

  def test_mergePolys(self):
    polys = []
    polys.append(Poly.createPolyFromRect(Rect(0, 1, 1, 4)))
    results = PolyMerger.mergePolys(polys)
    self.assertEquals(len(results), 1)
    self.assertListEqual(results[0].toPolygonArray(),
                         [[1, 1], [0, 1], [0, 4], [1, 4], [1, 1]])
                         
    polys = []
    polys.append(Poly.createPolyFromRect(Rect(0, 1, 1, 4)))
    polys.append(Poly.createPolyFromRect(Rect(1, 0, 2, 2)))
    results = PolyMerger.mergePolys(polys)
    self.assertEquals(len(results), 1)
    self.assertListEqual(results[0].toPolygonArray(),
                         [[2, 0], [1, 0], [1, 1], [0, 1], [0, 4], [1, 4],
                          [1, 2], [2, 2], [2, 0]])

    polys = []
    polys.append(Poly.createPolyFromRect(Rect(0, 1, 1, 4)))
    polys.append(Poly.createPolyFromRect(Rect(1, 0, 2, 2)))
    polys.append(Poly.createPolyFromRect(Rect(1, 3, 2, 5)))
    results = PolyMerger.mergePolys(polys)
    self.assertEquals(len(results), 1)
    self.assertListEqual(results[0].toPolygonArray(),
                         [[2, 3], [1, 3], [1, 2], [2, 2], [2, 0], [1, 0], [1, 1],
                          [0, 1], [0, 4], [1, 4], [1, 5], [2, 5], [2, 3]])

    polys = []
    polys.append(Poly.createPolyFromRect(Rect(0, 1, 1, 4)))
    polys.append(Poly.createPolyFromRect(Rect(1, 0, 2, 2)))
    polys.append(Poly.createPolyFromRect(Rect(1, 3, 2, 5)))
    polys.append(Poly.createPolyFromRect(Rect(2, 4, 3, 6)))
    results = PolyMerger.mergePolys(polys)
    self.assertEquals(len(results), 1)
    self.assertListEqual(results[0].toPolygonArray(),
                         [[3, 4], [2, 4], [2, 3], [1, 3], [1, 2], [2, 2], [2, 0], [1, 0], [1, 1],
                          [0, 1], [0, 4], [1, 4], [1, 5], [2, 5], [2, 6], [3, 6], [3, 4]])

    # polygon with a hole
    polys = []
    polys.append(Poly.createPolyFromRect(Rect(0, 1, 1, 4)))
    polys.append(Poly.createPolyFromRect(Rect(1, 0, 2, 2)))
    polys.append(Poly.createPolyFromRect(Rect(1, 3, 2, 5)))
    polys.append(Poly.createPolyFromRect(Rect(2, 1, 3, 4)))
    results = PolyMerger.mergePolys(polys)
    self.assertEquals(len(results), 1)
    self.assertListEqual(results[0].toPolygonArray(),
                         [[3, 1], [2, 1], [2, 0], [1, 0], [1, 1], [0, 1], [0, 4],
                          [1, 4], [1, 5], [2, 5], [2, 4], [3, 4], [3, 1]])

    polys = []
    polys.append(Poly.createPolyFromRect(Rect(0, 1, 1, 2)))
    polys.append(Poly.createPolyFromRect(Rect(0, 3, 1, 4)))
    polys.append(Poly.createPolyFromRect(Rect(1, 1, 2, 2)))
    polys.append(Poly.createPolyFromRect(Rect(1, 3, 2, 4)))
    polys.append(Poly.createPolyFromRect(Rect(2, 1, 3, 2)))
    results = PolyMerger.mergePolys(polys)
    self.assertEquals(len(results), 2)
    self.assertListEqual(results[0].toPolygonArray(),
                         [[2, 3], [1, 3], [0, 3], [0, 4], [1, 4], [2, 4], [2, 3]])
    self.assertListEqual(results[1].toPolygonArray(),
                         [[3, 1], [2, 1], [1, 1], [0, 1], [0, 2],
                          [1, 2], [2, 2], [3, 2], [3, 1]])

    polys = []
    polys.append(Poly.createPolyFromRect(Rect(0, 1, 1, 2)))
    polys.append(Poly.createPolyFromRect(Rect(0, 3, 1, 4)))
    polys.append(Poly.createPolyFromRect(Rect(1, 1, 2, 4)))
    polys.append(Poly.createPolyFromRect(Rect(2, 1, 3, 2)))
    polys.append(Poly.createPolyFromRect(Rect(2, 3, 3, 4)))
    polys.append(Poly.createPolyFromRect(Rect(3, 1, 4, 2)))
    results = PolyMerger.mergePolys(polys)
    self.assertEquals(len(results), 1)
    self.assertListEqual(results[0].toPolygonArray(),
                         [[4, 1], [3, 1], [2, 1], [1, 1], [0, 1], [0, 2], [1, 2],
                          [1, 3], [0, 3], [0, 4], [1, 4], [2, 4], [3, 4], [3, 3],
                          [2, 3], [2, 2], [3, 2], [4, 2], [4, 1]])

if __name__ == '__main__':
    logging.basicConfig(stream=sys.stderr)
    logging.getLogger('polygon').setLevel(logging.DEBUG)
    unittest.main()
