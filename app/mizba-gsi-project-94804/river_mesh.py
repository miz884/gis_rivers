import MySQLdb
import os
import webapp2
import json

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
            )
    cursor = db.cursor()
    cursor.execute(query, {'code':code})
    points = []
    for row in cursor.fetchall():
      points.append(row)

    self.response.write('%(callback)s && %(callback)s(%(json)s);\n'
                        % {'callback':str(callback), 'json':json.dumps(points)})
    db.close()


app = webapp2.WSGIApplication([
    ('/get_river', River),
    ('/get_river_mesh', RiverMesh),
    ])

