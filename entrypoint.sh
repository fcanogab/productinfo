#!/bin/bash
set -e

echo "Waiting for PostgreSQL at ${DBHOST}:${DBPORT:-5432}..."
while ! python -c "
import socket
s = socket.create_connection(('${DBHOST}', int('${DBPORT:-5432}')), timeout=2)
s.close()
" 2>/dev/null; do
    echo "  ...PostgreSQL not ready, retrying in 1s"
    sleep 1
done
echo "PostgreSQL is ready."

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Django application..."
exec gunicorn productinfo.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --timeout 120
