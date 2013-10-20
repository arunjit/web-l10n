# Copyright 2013 Arunjit Singh.

"""Language utilities for web-apps.

The primary goal of this module is to find the "best match" from a set
of languages to serve language-specific content.
"""

__author__ = 'Arunjit Singh <opensrc@ajsd.in>'

import re


# Language-range and quality from RFC2616. An assumption here is that
# quality is only specified if 0 <= q < 1
ACCEPT_LANGUAGE_RE = (
  r'([a-z]{1,8}(?:-[a-z]{1,8})?|\*)(?:;q=(0\.\d+|0))?'
)


def GetPreferredLanguages(accept_language):
  """Get list of preferred languages from an Accept-Language header.

  Args:
    accept_language: (str) The Accept-Language header.

  Returns:
    (list) Languages in order of their preference (highest first).
  """
  if not accept_language:
    return []

  accept_language = accept_language.lower().replace('_', '-')
  matches = re.findall(ACCEPT_LANGUAGE_RE, accept_language)
  if not matches:
    return []

  def q(x):
    return float(x[1]) if x[1] else 1.0
  locales = sorted(matches, key=q, reverse=True)
  return [locale[0] for locale in locales]


def GetBestMatch(accepted, available, default=None):
  """Gets the best match between accepted and available languages.

  Args:
    accepted: (str|list) An Accept-Language header or list of accepted
        languages in order of preference (see #GetPreferredLanguages).
    available: (list) A list of available languages. Each language
        should follow RFC2616. Example: [de, en, en-gb, fr-ca, fr-fr].
    default: (str) A default if no match was found.
  """
  if isinstance(accepted, str):
    accepted = GetPreferredLanguages(accepted)

  # available: de, en, en-gb, fr-ca, fr-fr
  # accepted: en; best-match: en
  # accepted: en-us; best-match: en

  prefixes = _CreatePrefixDict(available)

  for lang in accepted:
    lang = lang.replace('_', '-')
    # Check 1: direct match
    if lang in available:
      return lang
    # Check 2: prefix match
    prefix = _Prefix(lang)
    if prefix in prefixes:
      return prefixes[prefix][0]
  # Nothing found. Return the default
  return default


def _Prefix(lang):
  return lang.replace('_', '-').split('-')[0]


def _CreatePrefixDict(languages):
  ret = {}
  for lang in languages:
    prefix = _Prefix(lang)
    if prefix in ret:
      ret[prefix].append(lang)
    else:
      ret[prefix] = [lang]
  for prefix in ret:
    ret[prefix] = sorted(ret[prefix], key=len)
  return ret
