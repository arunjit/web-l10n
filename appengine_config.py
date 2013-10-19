# Copyright 2013 Arunjit Singh. All Rights Reserved.

"""App Engine configuration.

Adds AppStats middleware.
"""

__author__ = 'arunjitsingh'


appstats_DEBUG = True

appstats_CALC_RPC_COSTS = True


def webapp_add_wsgi_middleware(app):
  """Add AppStats recording."""
  from google.appengine.ext.appstats import recording
  app = recording.appstats_wsgi_middleware(app)
  return app
