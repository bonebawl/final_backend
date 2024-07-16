#!/usr/bin/env bash
# Exit on error
set -o errexit

# Add your build commands here
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate

# Start the application
gunicorn steam_api.wsgi:application
