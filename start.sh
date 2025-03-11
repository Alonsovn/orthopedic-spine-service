#! /usr/bin/env bash

# Turn on exit on error mode
set -e

# Turn on bash's job control mode
set -m

# Start Gunicorn
exec gunicorn -k uvicorn.workers.UvicornWorker -c ./src/gunicorn_config.py src.main:app &

# Start Celery worker process
#celery -A app.worker.celery worker --loglevel=INFO &

# Now we bring the primary process back into the foreground and leave it there
fg %1
