from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Actividad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=120)),
                ('tipo', models.CharField(choices=[('vocales', 'Vocales'), ('numeros', 'Números'), ('colores', 'Colores'), ('animales', 'Animales'), ('familia', 'Familia'), ('valores', 'Valores'), ('cuerpo', 'Cuerpo'), ('memoria', 'Memoria')], max_length=30)),
                ('descripcion', models.TextField(blank=True)),
                ('icono', models.CharField(blank=True, default='⭐', max_length=10)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rol', models.CharField(choices=[('admin', 'Administrador'), ('profesor', 'Profesor'), ('estudiante', 'Estudiante')], default='estudiante', max_length=20)),
                ('avatar', models.CharField(blank=True, default='🌈', max_length=10)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Progreso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('actividad', models.CharField(max_length=50)),
                ('puntaje', models.IntegerField(default=0)),
                ('detalle', models.CharField(blank=True, max_length=255)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='progreso', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Logro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=120)),
                ('descripcion', models.CharField(blank=True, max_length=255)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logros', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
