#!/bin/bash

ENV=$1

if [ x${ENV} = x ]
then
    echo "set env is development"
    ENV=development
fi

export FLASK_APP=main.py
export FLASK_ENV=${ENV}

echo "init database ..."
./scripts/init_db.sh

echo "adding some mock data into database ..."
invoke add

echo "Starting server ..."
flask run --host 0.0.0.0 # --debugger --reload
