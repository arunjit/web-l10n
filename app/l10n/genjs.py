
import os
import sys

JS = """
angular.module('localeMessages',['pascalprecht.translate']).
constant('currentLocale','%(locale)s').
config(['$translateProvider',function(t){t.translations(%(json)s)}]);
"""

IN_FMT = "locale_%s.json"
OUT_FMT = "locale_%s.js"

def main():
  if len(sys.argv) != 2:
    print("""Usage: python genjs.py <LOCALE>\n
      Example:
          $ python genjs.py en-us""")
    sys.exit(1)

  locale = sys.argv[1]
  json = ''

  infile = IN_FMT % locale
  with open(infile, 'r') as f:
    json = f.read().strip()

  if json:
    js = JS % dict(json=json, locale=locale)
    outfile = OUT_FMT % locale
    with open(outfile, 'w') as f:
      f.write(js)


if __name__ == '__main__':
  main()
