#!/usr/bin/env bash
# Exit on error
set -o errexit

# Instala las dependencias
pip install -r requirements.txt

# Delete DB (optional: if you want to restart the DB)
python manage.py flush --no-input

# Convert static asset files 
python manage.py collectstatic --no-input

# Apply any outstanding database migrations
python manage.py migrate

# Loadfixtures
python manage.py loaddata fixtures/fixtures.json
