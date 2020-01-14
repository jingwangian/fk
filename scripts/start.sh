#!/bin/bash

export FLASK_APP=main.py
export FLASK_ENV=prod

echo "init database ..."
./scripts/init_db.sh

# echo "adding some mock data into database ..."
# invoke add

echo "Starting server ..."
flask run --host 0.0.0.0 # --debugger --reload
