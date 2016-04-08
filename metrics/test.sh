#!/bin/sh
cd $VIRTUAL_ENV/src
coverage run --branch --source='.' manage.py test
coverage report > $VIRTUAL_ENV/metrics/coverage.txt
<<<<<<< HEAD
coverage html -d $VIRTUAL_ENV/metrics/coverage
=======
coverage html -d $VIRTUAL_ENV/metrics/coverage
>>>>>>> e09ab69b9b6f9c55cdf7daaee820454ad15e7c07
