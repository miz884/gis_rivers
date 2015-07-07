import math
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

def meshCodeToModifiedMeshCode(mesh_code):
  # from ppuuqvrwsx to ppqrsuuvwx
  code = ('0' + str(int(mesh_code)))[-10:]
  result = (
    code[0:2] +
    code[4:5] +
    code[6:7] +
    code[8:9] +
    code[2:4] +
    code[5:6] +
    code[7:8] +
    code[9:10])
  return int(result)


def modifiedMeshCodeToMeshCode(modified_mesh_code):
  code = ('0' + str(int(modified_mesh_code)))[-10:]
  # from ppqrsuuvwx to ppuuqvrwsx
  result = (
    code[0:2] +
    code[5:7] +
    code[2:3] +
    code[7:8] +
    code[3:4] +
    code[8:9] +
    code[4:5] +
    code[9:10])
  return int(result)


def modifiedMeshCodeToLatLng(modified_mesh_code):
  mesh_code = modifiedMeshCodeToMeshCode(modified_mesh_code)
  return meshCodeToLatLng(mesh_code)


def latLngToModifiedMeshCode(lat, lng):
  mesh_code = latLngToMeshCode(lat, lng)
  return meshCodeToModifiedMeshCode(mesh_code)


def meshCodeToLatLng(mesh_code):
  code = ('0' + str(int(mesh_code)))[-10:]
  # ppuuqvrwsx
  p = float(code[0:2])
  u = float(code[2:4])
  q = float(code[4:5])
  v = float(code[5:6])
  r = float(code[6:7])
  w = float(code[7:8])
  s = float(code[8:9])
  x = float(code[9:10])

  s = (40.0 * p) / 60.0 + (5.0 * q) / 60.0 + (30.0 * r + 3.0 * s) / 60.0 / 60.0
  w = 100.0 + u + (7.5 * v) / 60.0 + (45.0 * w + 4.5 * x) / 60.0 / 60.0
  
  n = s + 3.0 / 60.0 / 60.0
  e = w + 4.5 / 60.0 / 60.0

  return [float(s), float(w)]


def latLngToMeshCode(lat, lng):
  # lat
  t = float(lat) * 60.0
  a = t % 40.0
  p = int(t // 40.0)

  b = a % 5.0
  q = int(a // 5.0)

  t = b * 60.0
  c = t % 30.0
  r = int(t // 30.0)

  d = c % 3.0
  s = int(c // 3.0)

  # lng
  t = float(lng) - 100.0
  f = t % 1.0
  u = int(t // 1.0)

  t = f * 60.0
  g = t % 7.5
  v = int(t // 7.5)

  t = g * 60.0
  h = t % 45.0
  w = int(t // 45.0)

  i = h % 4.5
  x = int(h // 4.5)

  result = p
  result *= 100
  result += u
  result *= 10
  result += q
  result *= 10
  result += v
  result *= 10
  result += r
  result *= 10
  result += w
  result *= 10
  result += s
  result *= 10
  result += x

  return int(result)

