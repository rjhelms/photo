#!/bin/sh
pylint --load-plugins pylint_django -f text $VIRTUAL_ENV/src/photo > $VIRTUAL_ENV/metrics/pylint/photo.txt
pylint --load-plugins pylint_django -f text $VIRTUAL_ENV/src/photo_site > $VIRTUAL_ENV/metrics/pylint/photo_site.txt

