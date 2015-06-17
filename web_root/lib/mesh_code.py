import math
from decimal import *
import logging

# cf. http://www.stat.go.jp/data/mesh/pdf/gaiyo1.pdf

log = logging.getLogger('mesh_code')

'''
Modified Mesh Code:

The standard Mesh Codes are assigned locally.
The first 4 digits represent a primary area.
The next 2 digits represent a secondary area in a primary area.
And the next 2 digits represent an area of next level in a secondary area.
This is good to divide large data into small sections, but it is not easy
to order data globally in this format.
The format of 3rd level area code is: "ppuuqvrw", given that pp, q and r
represent latitude, uu, v and w represent longitude. In this format,
even if the code would be sorted in natural orders, the latitude and
longitude will be back and forth.

I'll introduce Modified Mesh Code in "ppqruuvw" format to sort data globally.
It can be sorted in natural orders, since the first 4 digits represent
latitude, then the remaining 4 digits represent longitude. If you iterate
on the code, you'll go horizontally (west to east) firstly, then count up
the latitude vertically (south to north).

e.g.
12345678
12  5 7  -> 1257
  34 6 8 -> 3468
--> 1257 3468

53394547
53  4 4  -> 5344
  39 5 7 -> 3957
--> 5344 3957

'''

d100 = Decimal(100)
d60 = Decimal(60)
d45 = Decimal(45)
d40 = Decimal(40)
d30 = Decimal(30)
d10 = Decimal(10)
d7_5 = (Decimal(75) / Decimal(10))
d5 = Decimal(5)
d1 = Decimal(1)


def meshCodeToModifiedMeshCode(mesh_code):
  code = int(mesh_code)
  # from ppuuqvrw to ppqruuvw
  w = Decimal(code % 10)
  code /= 10
  r = Decimal(code % 10)
  code /= 10
  v = Decimal(code % 10)
  code /= 10
  q = Decimal(code % 10)
  code /= 10
  u = Decimal(code % 100)
  code /= 100
  p = Decimal(code)

  result = p
  result *= d10
  result += q
  result *= d10
  result += r
  result *= d100
  result += u
  result *= d10
  result += v
  result *= d10
  result += w

  return int(result)


def modifiedMeshCodeToMeshCode(modified_mesh_code):
  code = int(modified_mesh_code)
  # from ppqruuvw to ppuuqvrw
  w = Decimal(code % 10)
  code /= 10
  v = Decimal(code % 10)
  code /= 10
  u = Decimal(code % 100)
  code /= 100
  r = Decimal(code % 10)
  code /= 10
  q = Decimal(code % 10)
  code /= 10
  p = Decimal(code)

  result = p
  result *= d100
  result += u
  result *= d10
  result += q
  result *= d10
  result += v
  result *= d10
  result += r
  result *= d10
  result += w

  return int(result)


def modifiedMeshCodeToSWNE(modified_mesh_code):
  mesh_code = modifiedMeshCodeToMeshCode(modified_mesh_code)
  return meshCodeToSWNE(mesh_code)


def latLngToModifiedMeshCode(lat, lng):
  mesh_code = latLngToMeshCode(lat, lng)
  return meshCodeToModifiedMeshCode(mesh_code)


def meshCodeToSWNE(mesh_code):
  code = int(mesh_code)
  w = Decimal(code % 10)
  code /= 10
  r = Decimal(code % 10)
  code /= 10
  v = Decimal(code % 10)
  code /= 10
  q = Decimal(code % 10)
  code /= 10
  u = Decimal(code % 100)
  code /= 100
  p = Decimal(code)

  log.debug([p, u, q, v, r, w])
  s = (d40 * p) / d60 + (d5 * q) / d60 + (d30 * r) / d60 / d60
  w = d100 + u + (d7_5 * v) / d60 + (d45 * w) / d60 / d60
  
  n = s + d30 / d60 / d60
  e = w + d45 / d60 / d60

  return [float(s), float(w), float(n), float(e)]


def latLngToMeshCode(lat, lng):
  # lat
  t = Decimal(lat) * d60
  a = t % d40
  p = t // d40

  b = a % d5
  q = a // d5

  t = b * d60
  c = t % d30
  r = t // d30

  # lng
  t = Decimal(lng) - d100
  f = t % d1
  u = t // d1

  t = f * d60
  g = t % d7_5
  v = t // d7_5

  t = g * d60
  h = t % d45
  w = t // d45

  result = p
  result *= d100
  result += u
  result *= d10
  result += q
  result *= d10
  result += v
  result *= d10
  result += r
  result *= d10
  result += w

  return int(result)

