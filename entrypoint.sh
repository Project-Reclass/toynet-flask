#!/usr/bin/env bash

source /app/environment/env-prod
flask init-db
flask run --host 0.0.0.0
