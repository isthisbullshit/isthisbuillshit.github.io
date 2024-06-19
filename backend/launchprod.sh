#!/usr/bin/env bash

. venv/bin/activate; gunicorn main:app --workers 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:80

