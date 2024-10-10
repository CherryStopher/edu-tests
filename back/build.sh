#!/usr/bin/env bash
# Exit on error
set -o errexit

# Instala las dependencias
pip install -r requirements.txt


# Convert static asset files 
python manage.py collectstatic --no-input

# Delete DB (optional: if you want to restart the DB)
python manage.py flush --no-input

# Apply any outstanding database migrations
python manage.py migrate

# Loadfixtures
python manage.py loaddata fixtures/fixtures.json

#  Create superuser
if [[ $CREATE_SUPERUSER ]];
then
  python manage.py createsuperuser --no-input
fi
