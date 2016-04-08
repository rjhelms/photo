#!/bin/sh

tail -n 2 -v $VIRTUAL_ENV/metrics/pylint/*.txt | grep -E -v '^[[:space:]]*$'
tail -c 6 -v $VIRTUAL_ENV/metrics/coverage.txt

