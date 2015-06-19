import json
import logging

E = 0.0001

_SOUTH = 1;
_WEST = 0;
_NORTH = 3;
_EAST = 2;

_SW = 0;
_SE = 1;
_NE = 2;
_NW = 3;

log = logging.getLogger('polygon')

def f_equals(f0, f1):
  return -E < (f0 - f1) and (f0 - f1) < E


class Rect:
  def __init__(self, south, west, north, east):
    self.south = south
    self.west = west
    self.north = north
    self.east = east

  def connectHorizontally(self, target):
    if (f_equals(self.south, target.south) and
        f_equals(self.north, target.north) and
        f_equals(self.east, target.west)):
      self.east = target.east
      return True
    else:
      return False

  def toPolygonArray(self):
    return ([[self.south, self.west],
             [self.south, self.east],
             [self.north, self.east],
             [self.north, self.west],
             [self.south, self.west]])


class PathPoint:
  def __init__(self, lat, lng):
    self.lat = lat
    self.lng = lng
    self.prev = None
    self.next = None

  def connectNext(self, target):
    self.next = target
    target.prev = self

  def connectPrev(self, target):
    self.prev = target
    target.next = self

  def toCoord(self):
    return [self.lat, self.lng]


class Path:
  def __init__(self):
    self.head = None
    self.tail = None

  @staticmethod
  def createPathFromRect(rect):
    _path = Path()
    _path.appendHead(PathPoint(rect.south, rect.west))
    _path.appendHead(PathPoint(rect.north, rect.west))
    _path.appendTail(PathPoint(rect.south, rect.east))
    _path.appendTail(PathPoint(rect.north, rect.east))
    return _path

  def appendHead(self, point):
    if self.head is None:
      self.tail = point
    else:
      self.head.connectNext(point);
    self.head = point

  def appendTail(self, point):
    if self.tail is None:
      self.head = point
    else:
      self.tail.connectPrev(point)
    self.tail = point

  def append(self, target):
    self.head.next = target.tail
    target.tail.prev = self.head

  def isOuterCircle(self):
    return (self.head.lng < self.tail.lng)

  def isInnerCircle(self):
    return not self.isOuterCircle()


class Poly:
  def __init__(self):
    self.path = None
    self.south = None
    self.west = None
    self.north = None
    self.east = None
    self.root = None
    self.finalized = False

  @staticmethod
  def createPolyFromRect(rect):
    _poly = Poly()
    path = Path.createPathFromRect(rect)
    _poly.path = path
    _poly.south = rect.south
    _poly.west = rect.west
    _poly.north = rect.north
    _poly.east = rect.east
    _poly.root = _poly
    return _poly

  def updateCoords(self):
    if self.finalized:
      raise Exception('Already finalized')
    self.north = self.path.head.lat
    self.east = self.path.tail.lng
    self.west = self.path.head.lng

  def isTouching(self, target):
    if not f_equals(self.north, target.south):
      return False
    return (self.west < target.east and
            self.east > target.west)

  # @param polys The array of poly in the next line.
  # @return True if any poly in polys are touching this Poly, False otherwise.
  def addPolys(self, polys):
    if self.finalized:
      raise Exception('Already finalized')
    isTouchingAnything = False
    for target in polys:
      if not self.isTouching(target):
        continue
      isTouchingAnything = True
      if self.path.head.next is None:
        self.path.head.connectNext(target.path.tail.next.next)
      else:
        target.path.tail.next.next.connectPrev(self.path.tail.prev)
      self.path.tail.connectPrev(target.path.tail.next)
      if target.root.south > self.root.south:
        target.root = self.root
      target.updateCoords()
    self.updateCoords()

    return isTouchingAnything

  def finalize(self):
    self.updateCoords()
    self.finalized = True
    self.path.head.next = self.path.tail
    self.path.tail.prev = self.path.head

  def toPolygonArray(self):
    result = []
    curr = self.path.head
    while (not curr is None):
      if (curr.next is None or
          curr.lat != curr.next.lat or
          curr.lng != curr.next.lng):
        result.append(curr.toCoord())
      if (len(result) > 1 and curr == self.path.head):
        break
      curr = curr.prev
    return result

  def isSamePoly(self, target):
    return self.root == target.root


class PolyMerger:

  # Merging squares horizontally if it's connecting each other.
  @staticmethod
  def mergeSquares(squares):
    rects = []
    curr = None
    for row in squares:
      target = Rect(row[_SOUTH], row[_WEST],
                    row[_NORTH], row[_EAST])
      if not curr:
        curr = target
        continue

      if not curr.connectHorizontally(target):
        rects.append(Poly.createPolyFromRect(curr))
        curr = target

    rects.append(Poly.createPolyFromRect(curr))
    return rects

  @staticmethod
  def mergePolys(polys):
    results = []
    prev = None
    curr = []
    for poly in polys:
      if (len(curr) == 0 or f_equals(curr[-1].north, poly.north)):
        curr.append(poly)
      elif prev is None:
        prev = curr
        curr = [poly]
      else:
        for poly0 in prev:
          if (not poly0.addPolys(curr)):
            poly0.finalize()
            results[:] = [x for x in results if not x.isSamePoly(poly0)]
            results.append(poly0)
        prev = curr
        curr = [poly]

    if not prev is None:
      for poly0 in prev:
        if (not poly0.addPolys(curr)):
          poly0.finalize()
          results[:] = [x for x in results if not x.isSamePoly(poly0)]
          results.append(poly0)

    for poly0 in curr:
      results[:] = [x for x in results if not x.isSamePoly(poly0)]

    results.extend(curr)
    return results

