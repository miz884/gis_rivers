import math
from decimal import *
import logging

# cf. http://www.stat.go.jp/data/mesh/pdf/gaiyo1.pdf

log = logging.getLogger('mesh_code')

d100 = Decimal(100)
d60 = Decimal(60)
d45 = Decimal(45)
d40 = Decimal(40)
d30 = Decimal(30)
d7_5 = (Decimal(75) / Decimal(10))
d5 = Decimal(5)
d1 = Decimal(1)


def meshcodeToSWNE(code):
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


def latLngToMeshcode(lat, lng):
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

  return int(
    1 * w +
    10 * r +
    100 * v +
    1000 * q +
    10000 * u +
    1000000 * p)

