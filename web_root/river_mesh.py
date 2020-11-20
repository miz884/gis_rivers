import MySQLdb
import os
import webapp2
import json
import polygon
import mesh_code
import mesh
import mesh_indexer
import pickle


class River(webapp2.RequestHandler):
  def _get_river_name(self, river_code):
    with open("./W07_river_mesh_index/river_code_index.dump", mode="rb") as f:
      index = pickle.load(f)
      if int(river_code) in index:
        return index[int(river_code)]
      else:
        return None

  def get(self):
    self.response.headers['Content-Type'] = 'text/javascript'

    lat = float(self.request.get('lat'))
    lng = float(self.request.get('lng'))
    callback = str(self.request.get('callback', 'callback'))

    if (lat == '' or lng == ''):
      self.response.write('%s && %s(false)\n' % (str(callback), str(callback)))
      return


    index_facade = mesh_indexer.MeshIndexFacade("./W07_river_mesh_index")
    modified_mesh_code = mesh_code.latLngToModifiedMeshCode(lat, lng)
    river_code = index_facade.search_by_modified_mesh_code(modified_mesh_code)

    if river_code is None:
      self.response.write('%s && %s(null);\n' % (str(callback), str(callback)))
    else:
      river_name = self._get_river_name(river_code)
      self.response.write('%s && %s("%s", %s);\n'
                          % (str(callback), str(callback), river_name, river_code))


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
      db = MySQLdb.connect(unix_socket='/cloudsql/mizba-gsi-project-94804:river-mesh',
                           user='root', db='river_mesh', charset='utf8')
    else:
      db = MySQLdb.connect(host='localhost', user='root')

    query = ('select mesh.modified_mesh_code'
             ' from river_mesh as mesh'
             ' where mesh.river_code = %(code)s'
             ' order by mesh.modified_mesh_code'
            )
    cursor = db.cursor()
    cursor.execute(query, {'code':code})

    code_list = []
    for row in cursor:
      code_list.append(row[0])

    result = mesh.MeshMerger.merge(code_list)
    lls = [map(lambda y: mesh_code.modifiedMeshCodeToLatLng(y), x) for x in result]

    self.response.write('%(callback)s && %(callback)s(%(json)s);\n'
                        % {'callback':str(callback),
                           'json':json.dumps(lls)})
    db.close()


app = webapp2.WSGIApplication([
    ('/get_river', River),
    ('/get_river_mesh', RiverMesh),
    ])

