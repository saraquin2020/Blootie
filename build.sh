#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate

# Carga la base de datos con las rutas correctas
python manage.py loaddata cuentos.json