# Copyright 2013 Arunjit Singh. All Rights Reserved.

"""Application configuration and App Engine context."""

__author__ = 'arunjitsingh'

import datetime
import os
import re

from google.appengine.api import app_identity

DEVELOPMENT = os.getenv('SERVER_SOFTWARE', '').startswith('Dev')
PRODUCTION = not DEVELOPMENT

if os.path.exists(os.path.join(os.path.dirname(__file__), '../FAKEPROD')):
  PRODUCTION = True

AUTH_DOMAIN = os.getenv('AUTH_DOMAIN', '')

_VERSION_ID = os.getenv('CURRENT_VERSION_ID', '0.0').split('.')
VERSION = _VERSION_ID[0]
VERSION_TIMESTAMP = int(_VERSION_ID[1]) >> 28
VERSION_DATETIME = datetime.datetime.fromtimestamp(VERSION_TIMESTAMP)

DEBUGGING = not PRODUCTION
if re.match(r'-(?:dev|debug|test)', VERSION):  # staging and prod are PRODUCTION
  DEBUGGING = True


# AppIdentity needs to be stubbed for tests, so this can't be defined globally.
def GetAppId():
  return app_identity.get_application_id()


WEBAPP2_CONFIG = {
    'webapp2_extras.jinja2': {
        'template_path': ['templates']
    },
    'webapp2_extras.sessions': {
        'secret_key': 'not really secret',
    },
}


# i18n
AVAILABLE_LOCALES = [
    'de-de',
    'en-us',
    'fr-fr',
]
DEFAULT_LOCALE = 'en-us'
LOCALE_PARAM = 'hl'
