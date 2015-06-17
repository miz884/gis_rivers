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
The format of 3rd level area code is: "ppuuqvrwsx", given that pp, q, r
and s represent latitude, uu, v, w and x represent longitude. In this format,
even if the code would be sorted in natural orders, the latitude and
longitude will be back and forth.

I'll introduce Modified Mesh Code in "ppqrsuuvwx" format to sort data globally.
It can be sorted in natural orders, since the first 5 digits represent
latitude, then the remaining 5 digits represent longitude. If you iterate
on the code, you'll go horizontally (west to east) firstly, then count up
the latitude vertically (south to north).

e.g.
1234567890
12  5 7 9  -> 12579
  34 6 8 0 -> 34680
--> 12579 34680

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
d4_5 = (Decimal(45) / Decimal(10))
d3 = Decimal(3)
d1 = Decimal(1)


def meshCodeToModifiedMeshCode(mesh_code):
  code = int(mesh_code)
  # from ppuuqvrwsx to ppqrsuuvwx
  x = Decimal(code % 10)
  code /= 10
  s = Decimal(code % 10)
  code /= 10
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
  result *= d10
  result += s
  result *= d100
  result += u
  result *= d10
  result += v
  result *= d10
  result += w
  result *= d10
  result += x

  return int(result)


def modifiedMeshCodeToMeshCode(modified_mesh_code):
  code = int(modified_mesh_code)
  # from ppqrsuuvwx to ppuuqvrwsx
  x = Decimal(code % 10)
  code /= 10
  w = Decimal(code % 10)
  code /= 10
  v = Decimal(code % 10)
  code /= 10
  u = Decimal(code % 100)
  code /= 100
  s = Decimal(code % 10)
  code /= 10
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
  result *= d10
  result += s
  result *= d10
  result += x

  return int(result)


def modifiedMeshCodeToSWNE(modified_mesh_code):
  mesh_code = modifiedMeshCodeToMeshCode(modified_mesh_code)
  return meshCodeToSWNE(mesh_code)


def latLngToModifiedMeshCode(lat, lng):
  mesh_code = latLngToMeshCode(lat, lng)
  return meshCodeToModifiedMeshCode(mesh_code)


def meshCodeToSWNE(mesh_code):
  code = int(mesh_code)
  x = Decimal(code % 10)
  code /= 10
  s = Decimal(code % 10)
  code /= 10
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

  log.debug([p, u, q, v, r, w, s, x])
  s = (d40 * p) / d60 + (d5 * q) / d60 + (d30 * r + d3 * s) / d60 / d60
  w = d100 + u + (d7_5 * v) / d60 + (d45 * w + d4_5 * x) / d60 / d60
  
  n = s + d3 / d60 / d60
  e = w + d4_5 / d60 / d60

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

  d = c % d3
  s = c // d3

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

  i = h % d4_5
  x = h // d4_5

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
  result *= d10
  result += s
  result *= d10
  result += x

  return int(result)

