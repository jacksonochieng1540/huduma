#!/bin/sh

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Creating superuser if it doesn't exist..."
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
username = "Vettle"
email = "admin@example.com"
password = "members"
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
EOF

echo "Starting Gunicorn server..."
exec gunicorn huduma.wsgi:application --bind 0.0.0.0:8000
