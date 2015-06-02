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
    rects = []
    r = None
    for row in cursor.fetchall():
      p = [row[0], row[1], row[2], row[3]]
      if not r:
        r = p
        continue

      if (f_equals(r[_SOUTH], p[_SOUTH]) and f_equals(r[_NORTH], p[_NORTH]) and
          f_equals(r[_EAST], p[_WEST])):
        r[_EAST] = p[_EAST]
      else:
        rects.append([[r[_SOUTH], r[_WEST]],
                      [r[_SOUTH], r[_EAST]],
                      [r[_NORTH], r[_EAST]],
                      [r[_NORTH], r[_WEST]],
                      [r[_SOUTH], r[_WEST]]])
        r = p

    rects.append([[r[_SOUTH], r[_WEST]],
                  [r[_SOUTH], r[_EAST]],
                  [r[_NORTH], r[_EAST]],
                  [r[_NORTH], r[_WEST]],
                  [r[_SOUTH], r[_WEST]]])

    self.response.write('%(callback)s && %(callback)s(%(json)s);\n'
                        % {'callback':str(callback), 'json':json.dumps(rects)})
    db.close()


app = webapp2.WSGIApplication([
    ('/get_river', River),
    ('/get_river_mesh', RiverMesh),
    ])

