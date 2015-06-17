# see https://cloud.google.com/appengine/docs/python/tools/libraries27#vendoring

from google.appengine.ext import vendor

# Add any libraries installed in the "lib" folder.
vendor.add('../lib')
