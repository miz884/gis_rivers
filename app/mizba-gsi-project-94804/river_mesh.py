import MySQLdb
import os
import webapp2
import json

E = 0.0001

_SOUTH = 1;
_WEST = 0;
_NORTH = 3;
_EAST = 2;

_SW = 0;
_SE = 1;
_NE = 2;
_NW = 3;

def f_equals(f0, f1):
  return -E < (f0 - f1) and (f0 - f1) < E

class River(webapp2.RequestHandler):
  def get(self):
    self.response.headers['Content-Type'] = 'text/javascript'

    lat = str(self.request.get('lat'))
    lng = str(self.request.get('lng'))
    callback = str(self.request.get('callback', 'callback'))

    if (lat == '' or lng == ''):
      self.response.write('%s && %s(false)\n' % (str(callback), str(callback)))
      return

    if (os.getenv('SERVER_SOFTWARE') and
      os.getenv('SERVER_SOFTWARE').startswith('Google App Engine/')):
      db = MySQLdb.connect(unix_socket='/cloudsql/mizba-gsi-project-94804:kanto-rivers',
                           user='root', db='kanto_rivers', charset='utf8')
    else:
      db = MySQLdb.connect(host='localhost', user='root')

    query = ('select river_code, river_name, min_lng, min_lat, max_lng, max_lat'
             ' from kanto_mesh'
             ' where %(lat)s between min_lat and max_lat'
             ' and %(lng)s between min_lng and max_lng'
            )
    cursor = db.cursor()
    cursor.execute(query, {'lat':lat, 'lng':lng})
    for row in cursor.fetchall():
      self.response.write('%s && %s("%s", "%s", %s, %s, %f, %f, %f, %f);\n'
                          % (str(callback), str(callback), row[0], row[1],
                             lng, lat, row[2], row[3], row[4], row[5]))

    db.close()


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


class RiverMesh(webapp2.RequestHandler):
  def get(self):
    self.response.headers['Content-Type'] = 'text/javascript'

    code = str(self.request.get('code'))
    callback = str(self.request.get('callback', 'callback'))

    if (code == ''):
      self.response.write('%s && %s(false)\n' % (str(callback), str(callback)))
      return

    if (os.getenv('SERVER_SOFTWARE') and
      os.getenv('SERVER_SOFTWARE').startswith('Google App Engine/')):
      db = MySQLdb.connect(unix_socket='/cloudsql/mizba-gsi-project-94804:kanto-rivers',
                           user='root', db='kanto_rivers', charset='utf8')
    else:
      db = MySQLdb.connect(host='localhost', user='root')

    query = ('select min_lng, min_lat, max_lng, max_lat'
             ' from kanto_mesh'
             ' where river_code = %(code)s'
             ' order by min_lat, min_lng'
            )
    cursor = db.cursor()
    cursor.execute(query, {'code':code})

    # phase 1.
    # Merging squares horizontally if it's connecting each other.
    rects = []
    curr = None
    for row in cursor.fetchall():
      target = Rect(row[_SOUTH], row[_WEST], row[_NORTH], row[_EAST])
      if not curr:
        curr = target
        continue

      connected = curr.connectHorizontally(target)
      if not connected:
        rects.append(curr.toPolygonArray())
        curr = target

    rects.append(curr.toPolygonArray())

    # phase2

    self.response.write('%(callback)s && %(callback)s(%(json)s);\n'
                        % {'callback':str(callback), 'json':json.dumps(rects)})
    db.close()


app = webapp2.WSGIApplication([
    ('/get_river', River),
    ('/get_river_mesh', RiverMesh),
    ])

