#!/bin/bash
# Render Build Script for Django

# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Create superuser (optional - uncomment if needed)
# python manage.py createsuperuser --noinput --username admin --email admin@example.com
