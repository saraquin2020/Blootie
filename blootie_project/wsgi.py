import os
from django.core.wsgi import get_wsgi_application
from dj_static import Cling, MediaCling

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blootie_project.settings')

# Esto obliga a Render a mostrar el diseño Y la carpeta media (fotos/audios)
application = Cling(MediaCling(get_wsgi_application()))