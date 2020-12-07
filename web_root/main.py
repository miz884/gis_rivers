import json
import os
import pickle
import pkg_resources
import sys

path = 'lib'
pkg_resources.working_set.add_entry(path)
sys.path.append(os.path.join(os.path.dirname(__file__), path))

import mesh_code
import mesh
import mesh_indexer

from flask import Flask
from flask import request
from flask import Response
from google.cloud import storage

app = Flask(__name__, static_folder='.', static_url_path='/')

def _get_river_name(river_code):
  with open("./data/W07_river_mesh_index/river_code_index.dump", mode="rb") as f:
    index = pickle.load(f, encoding='utf-8')
    if river_code in index:
      return index[river_code]
    else:
      return None

@app.route('/get_river')
def get_river():
  lat = float(request.args.get('lat'))
  lng = float(request.args.get('lng'))
  callback = str(request.args.get('callback', 'callback'))

  if (lat == '' or lng == ''):
    return Response('%s && %s(false)\n' % (str(callback), str(callback)),
                    content_type = 'text/javascript')

  index_facade = mesh_indexer.MeshIndexFacade("./data/W07_river_mesh_index")
  modified_mesh_code = mesh_code.latLngToModifiedMeshCode(lat, lng)
  river_code = index_facade.search_by_modified_mesh_code(modified_mesh_code)

  if river_code is None:
    return Response('%s && %s(null);\n' % (str(callback), str(callback)),
                    content_type = 'text/javascript')
  else:
    river_name = _get_river_name(river_code)
    return Response('%s && %s("%s", "%s");\n' % (str(callback),
                                                 str(callback),
                                                 river_name,
                                                 river_code),
                    content_type = 'text/javascript')


@app.route('/get_river_mesh')
def get_river_mesh():
  code = str(request.args.get('code'))
  callback = str(request.args.get('callback'))

  if (code == ''):
    return Response('%s && %s(false)\n' % (str(callback), str(callback)),
                    content_type = 'text/javascript')

  blob_name = "river_mesh_list/%s/%s" % (code[0:2], code)
  client = storage.Client(project='mizba-gsi-project-94804')
  bucket = client.bucket("gis_rivers")
  blob = bucket.blob(blob_name)
  content = blob.download_as_string()
  code_list = list(map(lambda y: int(y), content.splitlines()))

  result = mesh.MeshMerger.merge(code_list)
  lls = [list(map(lambda y: mesh_code.modifiedMeshCodeToLatLng(y), x)) for x in result]

  return Response(('%(callback)s && %(callback)s(%(json)s);\n' %
                    {'callback':str(callback), 'json':json.dumps(lls)}),
                    content_type = 'text/javascript')

if __name__ == '__main__':
  app.run(host='127.0.0.1', port=8080, debug=True)

