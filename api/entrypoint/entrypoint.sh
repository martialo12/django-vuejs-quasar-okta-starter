#!/bin/bash

# Migrate the database
python manage.py migrate

# Check if DEBUG is true or false
if [ "$DEBUG" = "true" ]; then
    # Run Gunicorn with the --reload flag
    gunicorn config.wsgi --bind 0.0.0.0:8000 --reload --config entrypoint/gunicorn.conf.py
else
    # Run Gunicorn without the --reload flag
    gunicorn config.wsgi --bind 0.0.0.0:8000 --config entrypoint/gunicorn.conf.py
fi
