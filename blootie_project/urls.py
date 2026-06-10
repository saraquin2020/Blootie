from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blootie_app.urls')),
    
    # ESTA LÍNEA ROMPE EL BLOQUEO: Fuerza a Render a mostrar los archivos de la carpeta media
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]