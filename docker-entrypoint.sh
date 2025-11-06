#!/bin/sh
set -eu

# If running behid gunicorn, run app migrations...
if [ "${1:-}" = "gunicorn" ]; then
    echo "Running migrations..."
    uv run manage.py migrate
fi

exec "$@"
