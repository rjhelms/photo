#!/bin/sh
pylint --load-plugins pylint_django -f html $VIRTUAL_ENV/src/photo > $VIRTUAL_ENV/metrics/pylint/photo.html
pylint --load-plugins pylint_django -f html $VIRTUAL_ENV/src/photo_site > $VIRTUAL_ENV/metrics/pylint/photo_site.html

