#!/bin/bash

echo "Start testing ..."
docker-compose run server pytest -v --cov-config=.coveragerc --cov-report=html --cov=app
echo "Done"
