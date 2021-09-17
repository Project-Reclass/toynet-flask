#!/usr/bin/env bash

source /app/environment/env-dev
flask init-db
pytest -v $1
