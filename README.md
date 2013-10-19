# web-l10n

Angular web-apps with localization.

## Build and run

This application uses [App Engine](https://developers.google.com/appengine),
though that was done for ease of deployment. Practically, this app could run
using any WSGI container (after stripping off the AE code). The AE code is
inconsequential for this demonstration.

Get the dependencies (requires [Bower](http://bower.io)):

    $ cd app
    $ bower install
    $ cd ..

Build dist:

    $ ./build

Run locally using `dev_appserver.py` (doesn't build dist):

    $ DEVAPPSERVER=/path/to/dev_appserver.py ./build run

Build and run locally from dist using `dev_appserver.py`:

    $ DEVAPPSERVER=/path/to/dev_appserver.py ./build runprod

## Deploy

You should change the application ID in `app.yaml` first.

    $ APPCFG=/path/to/appcfg.py ./build deploy
