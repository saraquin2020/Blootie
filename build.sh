#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# Este comando carga tus 8 cuentos automáticamente sin usar la Shell premium
python manage.py loaddata cuentos.json