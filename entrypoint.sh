#!/bin/sh
if [ "$1" = 'unittest' ]; then
    echo "Waiting for postgres..."

    while ! nc -z "${DB_HOST}" "${DB_PORT}"; do
      sleep 0.1
    done
    echo "PostgreSQL started"

    alembic upgrade head
    pytest --slow
    exit $?
elif [ "$1" = 'celery' ]; then
    echo "Starting celery worker..."
    celery -A core.celery worker -c${CELERY_WORKERS} --loglevel=INFO

else
    echo "Waiting for postgres..."

    while ! nc -z "${DB_HOST}" "${DB_PORT}"; do
      sleep 0.1
    done
    echo "PostgreSQL started"

    echo "Migrate the Database at startup of project"
    alembic upgrade head

    echo "Running uvicorn"
    gunicorn main:app -w ${GUNICORN_WORKERS} -k uvicorn.workers.UvicornWorker -b 0.0.0.0:5050 --access-logfile - --error-logfile - --log-level info
fi
