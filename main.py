# Copyright 2013 Arunjit Singh. All Rights Reserved.

"""The application's HTML pages."""

__author__ = 'arunjitsingh'

import webapp2

from server import config
from server import wsgi


class IndexPage(wsgi.RequestHandler):

  def get(self):
    self.Html().Write(self.RenderTemplate('index.html'))


app = webapp2.WSGIApplication([
        ('/', IndexPage),
    ],
    debug=config.DEBUGGING,
    config=config.WEBAPP2_CONFIG,
)
