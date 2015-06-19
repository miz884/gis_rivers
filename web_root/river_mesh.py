import MySQLdb
import os
import webapp2
import json
import polygon
import mesh_code


class River(webapp2.RequestHandler):
  def get(self):
    self.response.headers['Content-Type'] = 'text/javascript'

    lat = float(self.request.get('lat'))
    lng = float(self.request.get('lng'))
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

    query = ('select river.name, mesh.river_code '
             ' from compact_kanto_mesh as mesh'
             ' left join river_codes as river'
             ' on mesh.river_code = river.river_code'
             ' where mesh.modified_mesh_code = %(modified_mesh_code)s'
            )
    modified_mesh_code = mesh_code.latLngToModifiedMeshCode(lat, lng)
    cursor = db.cursor()
    count = cursor.execute(query, {'modified_mesh_code': modified_mesh_code})

    if count > 0:
      for row in cursor.fetchall():
        self.response.write('%s && %s("%s", %d);\n'
                            % (str(callback), str(callback), row[0], row[1]))
    else:
      self.response.write('%s && %s(null);\n' % (str(callback), str(callback)))

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

    # phase 1.
    # Merging squares horizontally if it's connecting each other.
    polys = polygon.PolyMerger.mergeSquares(cursor);

    # phase2
    result = polygon.PolyMerger.mergePolys(polys)

    self.response.write('%(callback)s && %(callback)s(%(json)s);\n'
                        % {'callback':str(callback),
                           'json':json.dumps(map(lambda x:x.toPolygonArray(),
                                                 result))})
    db.close()


app = webapp2.WSGIApplication([
    ('/get_river', River),
    ('/get_river_mesh', RiverMesh),
    ])

