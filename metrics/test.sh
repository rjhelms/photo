#!/bin/sh
cd $VIRTUAL_ENV/src
coverage run --branch --source='.' manage.py test
coverage report > $VIRTUAL_ENV/metrics/coverage.txt
