#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate

# Carga de datos esenciales para el Centro de Control del Profesor
python manage.py loaddata usuarios.json
python manage.py loaddata perfiles.json
python manage.py loaddata cuentos.json