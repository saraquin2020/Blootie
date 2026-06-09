from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from blootie_app.models import Perfil, Actividad

class Command(BaseCommand):
    help = 'Carga datos demo de Blootie'

    def handle(self, *args, **kwargs):
        admin, _ = User.objects.get_or_create(username='admin', defaults={'first_name': 'Administrador', 'last_name': 'Blootie', 'is_staff': True, 'is_superuser': True})
        admin.set_password('admin123')
        admin.is_staff = True
        admin.is_superuser = True
        admin.save()
        Perfil.objects.get_or_create(user=admin, defaults={'rol': 'admin', 'avatar': '🌈'})

        profe, _ = User.objects.get_or_create(username='profe', defaults={'first_name': 'Profe', 'last_name': 'Blootie'})
        profe.set_password('profe123')
        profe.save()
        Perfil.objects.get_or_create(user=profe, defaults={'rol': 'profesor', 'avatar': '👩‍🏫'})

        nina, _ = User.objects.get_or_create(username='nina1', defaults={'first_name': 'Nina', 'last_name': 'Blootie'})
        nina.set_password('nina123')
        nina.save()
        Perfil.objects.get_or_create(user=nina, defaults={'rol': 'estudiante', 'avatar': '🧒'})

        actividades = [
            ('Reconocer las vocales', 'vocales', 'Aprender A, E, I, O, U con apoyo visual.', '🔤'),
            ('Contar del 1 al 5', 'numeros', 'Reconocer números y cantidades básicas.', '🔢'),
            ('Mis colores favoritos', 'colores', 'Identificar rojo, azul, amarillo y verde.', '🎨'),
            ('Animales amigables', 'animales', 'Identificar animales comunes con apoyo visual.', '🐻'),
            ('Mi familia', 'familia', 'Reconocer miembros cercanos de la familia.', '👨‍👩‍👧'),
            ('Valores bonitos', 'valores', 'Respeto, amor, amistad y compartir.', '💛'),
            ('Partes del cuerpo', 'cuerpo', 'Conocer ojos, nariz, orejas y manos.', '🧍'),
            ('Juego de memoria', 'memoria', 'Asociar parejas visuales.', '🧠'),
        ]
        for titulo, tipo, descripcion, icono in actividades:
            Actividad.objects.get_or_create(titulo=titulo, defaults={'tipo': tipo, 'descripcion': descripcion, 'icono': icono})

        self.stdout.write(self.style.SUCCESS('Datos demo cargados correctamente.'))
