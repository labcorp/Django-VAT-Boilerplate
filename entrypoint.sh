#!/bin/bash -e
./manage.py migrate

# If running gunicorn the migrate existing database
if [ "${@: -2:1}" == "gunicorn" ]; then
    ./manage.py collectstatic --clear --noinput
    ./manage.py migrate
fi

exec "${@}"
