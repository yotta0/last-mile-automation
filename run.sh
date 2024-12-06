#!/bin/sh

export PYTHONPATH=$(pwd)
export FLASK_APP=src/main.py

alembic upgrade head

flask run --host=0.0.0.0 --port=5000
