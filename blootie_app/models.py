from django.db import models
from django.contrib.auth.models import User

# --- PERFIL DE USUARIO ---
class Perfil(models.Model):
    ROL_CHOICES = [
        ('admin', 'Administrador'),
        ('profesor', 'Profesor'),
        ('estudiante', 'Estudiante'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.CharField(max_length=20, choices=ROL_CHOICES, default='estudiante')
    avatar = models.CharField(max_length=10, blank=True, default='🌈')
    
    profesor_asignado = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='mis_estudiantes',
        limit_choices_to={'perfil__rol': 'profesor'}
    )

    def __str__(self):
        return f"{self.user.username} - {self.rol}"

# --- BIBLIOTECA DE CONTENIDOS ---
class Actividad(models.Model):
    TIPO_CHOICES = [
        ('vocales', 'Vocales'),
        ('numeros', 'Números'),
        ('colores', 'Colores'),
        ('animales', 'Animales'),
        ('familia', 'Familia'),
        ('valores', 'Valores'),
        ('cuerpo', 'Cuerpo'),
        ('memoria', 'Memoria'),
    ]
    titulo = models.CharField(max_length=120)
    tipo = models.CharField(max_length=30, choices=TIPO_CHOICES)
    descripcion = models.TextField(blank=True)
    icono = models.CharField(max_length=10, blank=True, default='⭐')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    creado_por = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='actividades_creadas'
    )

    def __str__(self):
        return self.titulo

# --- SEGUIMIENTO DE PROGRESO ---
class Progreso(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progreso')
    
    actividad_ref = models.ForeignKey(
        Actividad, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='registros_progreso'
    )
    
    actividad = models.CharField(max_length=50) 
    puntaje = models.IntegerField(default=0)
    detalle = models.CharField(max_length=255, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.actividad}"

# --- SISTEMA DE LOGROS ---
class Logro(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='logros')
    nombre = models.CharField(max_length=120)
    descripcion = models.CharField(max_length=255, blank=True)
    icono = models.CharField(max_length=10, default='🏆') 
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.nombre}"

class ConfiguracionActividad(models.Model):
    nombre = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    esta_activa = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

# ESTA LÍNEA DEBE IR SIN ESPACIOS AL PRINCIPIO
class Cuento(models.Model):
    titulo = models.CharField(max_length=200)
    portada = models.ImageField(upload_to='cuentos/portadas/')
    contenido = models.TextField() 
    audio = models.FileField(upload_to='cuentos/audios/', blank=True, null=True)

    def __str__(self):
        return self.titulo