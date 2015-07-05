import logging

# cf. http://www.stat.go.jp/data/mesh/pdf/gaiyo1.pdf

log = logging.getLogger('mesh')

# In this package, all mesh code should be considered as a modified mesh
# code (ppqrsuuvwx) unless it would be explicitly mentioned as a standard
# mesh code (ppuuqvrwsx).


class Mesh:

  cache = {}

  def __init__(self, code):
    self.code = code

  def __eq__(self, target):
    if isinstance(target, Mesh):
      return self.code == target.code
    else:
      return NotImplemented

  def __ne__(self, target):
    if isinstance(target, Mesh):
      return self.code != target.code
    else:
      return NotImplemented

  def __lt__(self, target):
    if isinstance(target, Mesh):
      return self.code < target.code
    else:
      return NotImplemented

  def __gt__(self, target):
    if isinstance(target, Mesh):
      return self.code > target.code
    else:
      return NotImplemented

  def __le__(self, target):
    if isinstance(target, Mesh):
      return self.code <= target.code
    else:
      return NotImplemented

  def __ge__(self, target):
    if isinstance(target, Mesh):
      return self.code >= target.code
    else:
      return NotImplemented

  @staticmethod
  def get(code):
    if code in Mesh.cache:
      return Mesh.cache[code]
    else:
      instance = Mesh(code)
      Mesh.cache[code] = instance
      return instance

  def south(self):
    return Mesh.get(self.code - 100000)

  def north(self):
    return Mesh.get(self.code + 100000)

  def west(self):
    return Mesh.get(self.code - 1)

  def east(self):
    return Mesh.get(self.code + 1)


class MeshMerger:

  @staticmethod
  def merge(code_list):
    if len(code_list) == 0:
      return

    # 1st phase: merge mesh
    mesh_hash = {}
    start_points = []
    for code in code_list:
      mesh = Mesh.get(code)
      touching_list = [mesh_hash[x.code] for x in [mesh.south(),
                                                   mesh.north(),
                                                   mesh.east(),
                                                   mesh.west()] if x.code in mesh_hash]
      touching_list.append(mesh)
      start_points[:] = [x for x in start_points if x not in touching_list]
      mesh_hash[code] = min(touching_list)
      start_points.append(mesh_hash[code])

    # 2nd phase: trace edge
    lines = []
    for start in start_points:
      prev = None
      curr = start
      line = [curr.code]
      while True:
        nexts = MeshMerger._calcNextCornerCodes(curr, mesh_hash)
        if len(nexts) == 1:
          next = nexts[0]
        else:
          if not prev:
            next = curr.north()
          else:
            d = curr.code - prev.code
            if d == -1:
              next = curr.north()
            elif d == 1:
              next = curr.south()
            elif d == -100000:
              next = curr.west()
            elif d == 100000:
              next = curr.east()
            else:
              raise Exception('Invalid d ' + d)
        line.append(next.code)
        if (next == start):
          break
        prev = curr
        curr = next
      lines.append(line)

    return lines

  
  # @param corner_code Mesh
  # @param mesh_hash Dictionary<integer, Mesh>
  @staticmethod
  def _calcNextCornerCodes(corner_code, mesh_hash):
    # X: THE corner
    #
    # 1.UL | 2.UR
    # -----X-----
    # 4.LL | 3.LR
    #
    # code: 0b4321

    code = (0b0001 * (corner_code.west().code in mesh_hash) +
            0b0010 * (corner_code.code in mesh_hash) +
            0b0100 * (corner_code.south().code in mesh_hash) +
            0b1000 * (corner_code.south().west().code in mesh_hash))

    results = []
    if code & 0b1001 == 0b0001:
      results.append(corner_code.west())
    if code & 0b0011 == 0b0010:
      results.append(corner_code.north())
    if code & 0b0110 == 0b0100:
      results.append(corner_code.east())
    if code & 0b1100 == 0b1000:
      results.append(corner_code.south())
    if code == 0b0000:
      raise Exception('Empty matrix at ' + upper_right)
    if code == 0b1111:
      raise Exception('Full matrix at ' + upper_right)
    if not results:
      raise Exception('Unknown state')

    return results

