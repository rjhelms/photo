#!/bin/sh
cd $VIRTUAL_ENV/src
coverage run --branch --source='.' manage.py test
coverage html -d $VIRTUAL_ENV/metrics/coverage

