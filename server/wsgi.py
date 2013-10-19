# Copyright 2013 Arunjit Singh. All Rights Reserved.

"""Base WSGI, with templates, sessions, RequestHandler, JSON and users."""
from server import config

__author__ = 'arunjitsingh'

import json

from google.appengine.api import users

import webapp2
from webapp2_extras import jinja2
from webapp2_extras import sessions
from webapp2_extras.appengine import sessions_memcache


JSON_XSSI_PREFIX = ')]}\',\n'


class RequestHandler(webapp2.RequestHandler):

  def __init__(self, *args, **kwds):
    super(RequestHandler, self).__init__(*args, **kwds)
    self.user = users.get_current_user()
    self.is_user_admin = users.is_current_user_admin()
    self.app_id = config.GetAppId()


  ## Templates

  @webapp2.cached_property
  def jinja2(self):
    """A jinja2 object with an environment configured from the current app."""
    return jinja2.get_jinja2(app=self.app)

  def GetTemplate(self, name):
    """Gets a template.

    Args:
      name: (str) The name of the template.

    Returns:
      (jinja2.Template) The template.

    Raises:
      jinja2.TemplateError: Error getting the template (like TemplateNotFound).
    """
    return self.jinja2.environment.get_template(name)

  def Html(self):
    self.response.headers.add_header('Content-Type', 'text/html; charset=utf-8')
    return self

  def RenderTemplate(self, name, data=None):
    """Renders a template."""
    template = self.GetTemplate(name)
    data = data or {}
    data.update(
        PRODUCTION=config.PRODUCTION,
        DEBUGGING=config.DEBUGGING,
        APP_ID=self.app_id,
        VERSION=config.VERSION,
        VERSION_TIMESTAMP=config.VERSION_TIMESTAMP,
        ADMIN=self.is_user_admin,
        LOCALE=self.GetLocale(),
        user_name=self.user.nickname() if self.user else '',
        user_email=self.user.email() if self.user else '',
    )
    return template.render(data)


  ## JSON

  def Json(self):
    self.response.headers.add_header(
        'Content-Type', 'application/json; charset=utf-8')
    return self

  def RenderJson(self, data=None):
    data = data or {}
    return JSON_XSSI_PREFIX + json.dumps(data)


  ## Response

  def Write(self, data):
    self.response.write(data)
    return self

  ## i18n

  def GetLocale(self):
    locale = self.request.get(config.LOCALE_PARAM, '').replace('_', '-')
    if locale in config.AVAILABLE_LOCALES:
      return locale
    return config.DEFAULT_LOCALE


  ## Sessions

  # Overrides webapp2.RequestHandler#dispatch
  def dispatch(self):
    # Get a session store for this request.
    self.session_store = sessions.get_store(request=self.request)

    try:
      # Dispatch the request.
      webapp2.RequestHandler.dispatch(self)
    finally:
      # Save all sessions.
      self.session_store.save_sessions(self.response)

  @webapp2.cached_property
  def session(self):
    return self.session_store.get_session(
        factory=sessions_memcache.MemcacheSessionFactory)
