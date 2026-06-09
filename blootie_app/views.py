from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count, Sum
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404

from .forms import LoginForm
from .models import Perfil, Actividad, Progreso, Logro, ConfiguracionActividad, Cuento


MODULES = {
    'vocales': {'emoji': '🔤', 'title': 'Vocales', 'gradient': 'gradient-pink', 'lead': 'Observa y repite las vocales: A, E, I, O, U.', 'cards': [('A', 'Avión ✈️'), ('E', 'Elefante 🐘'), ('I', 'Iglesia ⛪'), ('O', 'Oso 🐻'), ('U', 'Uvas 🍇')], 'logro': 'Explorador de vocales', 'detalle': 'Reconoció las vocales básicas.'},
    'numeros': {'emoji': '🔢', 'title': 'Números', 'gradient': 'gradient-blue', 'lead': 'Cuenta del 1 al 5 con apoyo visual.', 'cards': [('1', '🍎'), ('2', '🍎🍎'), ('3', '🍎🍎🍎'), ('4', '🍎🍎🍎🍎'), ('5', '🍎🍎🍎🍎🍎')], 'logro': 'Genio de los números', 'detalle': 'Contó números del 1 al 5.'},
    'colores': {'emoji': '🎨', 'title': 'Colores', 'gradient': 'gradient-yellow', 'lead': 'Reconoce colores principales.', 'cards': [('Rojo', ''), ('Azul', ''), ('Amarillo', ''), ('Verde', '')], 'logro': 'Artista del color', 'detalle': 'Reconoció colores básicos.'},
    'animales': {'emoji': '🐻', 'title': 'Animales', 'gradient': 'gradient-green', 'lead': 'Identifica animales amigables.', 'cards': [('🐶', 'Perro'), ('🐱', 'Gato'), ('🐰', 'Conejo'), ('🐻', 'Oso')], 'logro': 'Amigo de los animales', 'detalle': 'Identificó animales.'},
    'familia': {'emoji': '👨‍👩‍👧', 'title': 'Familia', 'gradient': 'gradient-purple', 'lead': 'Reconoce miembros de la family.', 'cards': [('👩', 'Mamá'), ('👨', 'Papá'), ('👧', 'Hija'), ('👦', 'Hijo')], 'logro': 'Mi familia hermosa', 'detalle': 'Reconoció miembros de la familia.'},
    'valores': {'emoji': '💛', 'title': 'Valores', 'gradient': 'gradient-orange', 'lead': 'Aprende valores bonitos.', 'cards': [('🤝', 'Respeto'), ('💖', 'Amor'), ('😊', 'Amistad'), ('🎁', 'Compartir')], 'logro': 'Corazón amable', 'detalle': 'Reconoció valores.'},
    'cuerpo': {'emoji': '🧍', 'title': 'Cuerpo', 'gradient': 'gradient-teal', 'lead': 'Conoce partes del cuerpo.', 'cards': [('👀', 'Ojos'), ('👃', 'Nariz'), ('👂', 'Orejas'), ('🖐️', 'Manos')], 'logro': 'Conozco mi cuerpo', 'detalle': 'Reconoció partes del cuerpo.'},
}

MODULES_CANCIONES = {
    'c01': {'id': 'c01', 'title': 'Las Vocales', 'url': 'https://www.youtube.com/embed/SYY357gVkSg'},
    'c02': {'id': 'c02', 'title': 'Abejita Chiquitita', 'url': 'https://www.youtube.com/embed/Bya-v3tww7o'},
    'c03': {'id': 'c03', 'title': 'Palomita Blanca', 'url': 'https://www.youtube.com/embed/9QHSmIvbKR8'},
    'c04': {'id': 'c04', 'title': 'El Sapo', 'url': 'https://www.youtube.com/embed/6rbX0JT98ms'},
    'c05': {'id': 'c05', 'title': 'Mariposita', 'url': 'https://www.youtube.com/embed/QRa9On5_grA'},
    'c06': {'id': 'c06', 'title': 'Los Pollitos Dicen', 'url': 'https://www.youtube.com/embed/qcOiqtMsjes'},
    'c7': {'id': 'c7', 'title': 'Perro Amigo', 'url': 'https://www.youtube.com/embed/eMvt0ikkbkg'},
    'c8': {'id': 'c8', 'title': 'Mariana', 'url': 'https://www.youtube.com/embed/LMJLfZH_xWU'},
    'c9': {'id': 'c9', 'title': 'Cucarachita', 'url': 'https://www.youtube.com/embed/EWmvCS0pT9k'},
    'c10': {'id': 'c10', 'title': 'Arroz con leche', 'url': 'https://www.youtube.com/embed/4tzyWwcb1f0'},
    'c11': {'id': 'c11', 'title': 'La gallina turuleca', 'url': 'https://www.youtube.com/embed/jV2GUIIW2UE'},
    'c12': {'id': 'c12', 'title': 'Debajo de un botón', 'url': 'https://www.youtube.com/embed/q5IEuQ0GE-4'},
    'c13': {'id': 'c13', 'title': 'Mambrú se fue a la guerra', 'url': 'https://www.youtube.com/embed/zOnyeaHK8ng'},
    'c14': {'id': 'c14', 'title': 'Al corro de la patata', 'url': 'https://www.youtube.com/embed/UHuMcUaj4i8'},
    'c15': {'id': 'c15', 'title': 'Pollito Amarillito', 'url': 'https://www.youtube.com/embed/z1gFMujtH-o'},
    'c16': {'id': 'c16', 'title': 'Pin Pon', 'url': 'https://www.youtube.com/embed/RX0VtkQOddw'},
}

@login_required
def redirect_by_role(request):
    username = request.user.username.lower()
    if request.user.is_superuser:
        return redirect('admin_dashboard')
    if username.startswith('profe'):
        return redirect('teacher_dashboard')
    return redirect('student_dashboard')

def require_role(user, allowed):
    if user.is_superuser:
        return True
    username = user.username.lower()
    if username.startswith('profe'):
        role = 'profesor'
    else:
        role = 'estudiante'
    return role in allowed

def home(request):
    actividades = Actividad.objects.all()[:8]
    return render(request, 'home.html', {'actividades': actividades, 'modules': MODULES})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('redirect_by_role')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('redirect_by_role')
    else:
        form = LoginForm(request)
    return render(request, 'login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def admin_dashboard(request):
    if not require_role(request.user, ['admin']):
        return HttpResponseForbidden('Acceso denegado.')
    return render(request, 'admin/dashboard.html', {
        'total_usuarios': User.objects.count(),
        'total_profesores': Perfil.objects.filter(rol='profesor').count(),
        'total_estudiantes': Perfil.objects.filter(rol='estudiante').count(),
        'total_actividades': Actividad.objects.count(),
    })

@login_required
def admin_users(request):
    if not require_role(request.user, ['admin']):
        return HttpResponseForbidden('Acceso denegado.')
    return render(request, 'admin/users.html', {'usuarios': User.objects.all().order_by('-id')})

@login_required
def admin_activities(request):
    if not require_role(request.user, ['admin']):
        return HttpResponseForbidden('Acceso denegado.')
    return render(request, 'admin/activities.html', {'actividades': Actividad.objects.all().order_by('-id')})

@login_required
def teacher_dashboard(request):
    if not require_role(request.user, ['profesor', 'admin']):
        return HttpResponseForbidden('Acceso denegado.')
    return render(request, 'teacher/dashboard.html', {
        'estudiantes': Perfil.objects.filter(rol='estudiante').count(),
        'progreso': Progreso.objects.count(),
        'logros': Logro.objects.count(),
    })

@login_required
def teacher_students(request):
    if not require_role(request.user, ['profesor', 'admin']):
        return HttpResponseForbidden('Acceso denegado.')
    estudiantes = User.objects.filter(perfil__rol='estudiante').annotate(
        actividades_realizadas=Count('progreso'),
        puntaje_total=Sum('progreso__puntaje')
    ).order_by('username')
    return render(request, 'teacher/students.html', {'estudiantes': estudiantes})

@login_required
def teacher_activities(request):
    if not require_role(request.user, ['profesor', 'admin']):
        return HttpResponseForbidden('Acceso denegado.')
    return render(request, 'teacher/activities.html', {'actividades': Actividad.objects.all().order_by('tipo', 'titulo')})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.first_name = user.username.capitalize() 
            user.save()

            # Crea el perfil limpio con el rol de estudiante asignado correctamente
            Perfil.objects.create(
                user=user, 
                rol='estudiante',
            )
            messages.success(request, "¡Estudiante registrado con éxito! 🎉")
            return redirect('login')
    else:
        form = UserCreationForm()
        for field in form.fields.values():
            field.help_text = None 
            
    return render(request, 'student/register.html', {'form': form})
@login_required
def student_memory(request):
    if not require_role(request.user, ['estudiante', 'profesor', 'admin']):
        return HttpResponseForbidden('Acceso denegado.')
    
    if not ConfiguracionActividad.objects.filter(nombre='Memoria', esta_activa=True).exists() and not request.user.is_superuser:
        messages.error(request, 'El juego de Memoria está cerrado por el profesor en este momento. 🔒')
        return redirect('student_dashboard')

    if request.method == 'POST':
        # SOLUCIÓN DEFINITIVA: Se cambia 'activity' por 'actividad'
        Progreso.objects.create(
            usuario=request.user, 
            actividad='memoria', 
            puntaje=10, 
            detalle='Jugó memoria.'
        )
        Logro.objects.get_or_create(
            usuario=request.user, 
            nombre='Mente brillante', 
            defaults={'descripcion': 'Completó el juego de memoria.'}
        )
        messages.success(request, '¡Excelente! Registraste la memoria.')
        return redirect('student_dashboard') # Te regresa al panel del alumno mostrando su mensaje de éxito
        
    return render(request, 'student/memory.html')

@login_required
def student_achievements(request):
    if not require_role(request.user, ['estudiante', 'profesor', 'admin']):
        return HttpResponseForbidden('Acceso denegado.')
    return render(request, 'student/achievements.html', {'logros': Logro.objects.filter(usuario=request.user).order_by('-id')})

# --- VISTAS DE JUEGOS CON CANDADOS UNIFICADOS ---

@login_required
def game_bubbles(request): 
    if not require_role(request.user, ['estudiante', 'profesor', 'admin']):
        return HttpResponseForbidden('Acceso denegado.')
    
    if not ConfiguracionActividad.objects.filter(nombre='Vocales', esta_activa=True).exists() and not request.user.is_superuser:
        messages.error(request, 'El juego de Vocales (Burbujas) está cerrado por el profesor en este momento. 🔒')
        return redirect('student_dashboard')

    return render(request, 'student/game_bubbles.html')

@login_required
def game_numbers(request): 
    if not require_role(request.user, ['estudiante', 'profesor', 'admin']):
        return HttpResponseForbidden('Acceso denegado.')
    
    if not ConfiguracionActividad.objects.filter(nombre='Matemáticas', esta_activa=True).exists() and not request.user.is_superuser:
        messages.error(request, 'El juego de Números está cerrado por el profesor en este momento. 🔒')
        return redirect('student_dashboard')

    return render(request, 'student/game_numbers.html')

@login_required
def game_colors(request): 
    if not require_role(request.user, ['estudiante', 'profesor', 'admin']):
        return HttpResponseForbidden('Acceso denegado.')
    
    if not ConfiguracionActividad.objects.filter(nombre='Colores', esta_activa=True).exists() and not request.user.is_superuser:
        messages.error(request, 'El juego de Colores está cerrado por el profesor en este momento. 🔒')
        return redirect('student_dashboard')

    return render(request, 'student/game_colors.html')

@login_required
def game_animals(request):
    if not require_role(request.user, ['estudiante', 'profesor', 'admin']):
        return HttpResponseForbidden('Acceso denegado.')
    
    if not ConfiguracionActividad.objects.filter(nombre='Animales', esta_activa=True).exists() and not request.user.is_superuser:
        messages.error(request, 'El juego de Animales está cerrado por el profesor en este momento. 🔒')
        return redirect('student_dashboard')

    context = {
        'module': MODULES.get('animales')
    }
    return render(request, 'student/game_animals.html', context)

@login_required
def game_family(request): 
    if not require_role(request.user, ['estudiante', 'profesor', 'admin']):
        return HttpResponseForbidden('Acceso denegado.')
    
    if not ConfiguracionActividad.objects.filter(nombre='Familia', esta_activa=True).exists() and not request.user.is_superuser:
        messages.error(request, 'El juego de la Familia está cerrado por el profesor en este momento. 🔒')
        return redirect('student_dashboard')

    return render(request, 'student/game_family.html')

@login_required
def game_values(request): 
    if not require_role(request.user, ['estudiante', 'profesor', 'admin']):
        return HttpResponseForbidden('Acceso denegado.')
    
    if not ConfiguracionActividad.objects.filter(nombre='Valores', esta_activa=True).exists() and not request.user.is_superuser:
        messages.error(request, 'El juego de Valores está cerrado por el profesor en este momento. 🔒')
        return redirect('student_dashboard')

    return render(request, 'student/game_values.html')

@login_required
def game_body(request): 
    if not require_role(request.user, ['estudiante', 'profesor', 'admin']):
        return HttpResponseForbidden('Acceso denegado.')
    
    if not ConfiguracionActividad.objects.filter(nombre='Cuerpo', esta_activa=True).exists() and not request.user.is_superuser:
        messages.error(request, 'El juego del Cuerpo está cerrado por el profesor en este momento. 🔒')
        return redirect('student_dashboard')

    return render(request, 'student/game_body.html')

@login_required
def teacher_panel(request):
    mis_estudiantes = Perfil.objects.filter(rol='estudiante')
    estudiantes_ids = mis_estudiantes.values_list('user_id', flat=True)

    context = {
        'estudiantes': mis_estudiantes.count(),
        'progreso': Progreso.objects.filter(usuario_id__in=estudiantes_ids).count(),
        'logros': Logro.objects.filter(usuario_id__in=estudiantes_ids).count(),
        'actividades_recientes': Progreso.objects.filter(
            usuario_id__in=estudiantes_ids
        ).order_by('-fecha_creacion')[:5],
        'labels_grafico': ["Vocales", "Números", "Colores"],
        'data_grafico': [10, 15, 8],
    }
    return render(request, 'teacher/panel.html', context)

@login_required
def lista_alumnos(request):
    alumnos = Perfil.objects.filter(rol='estudiante')
    query = request.GET.get('q')
    if query:
        alumnos = alumnos.filter(user__username__icontains=query)

    context = {
        'alumnos': alumnos,
    }
    return render(request, 'teacher/students.html', context)

@login_required
def detalle_alumno(request, alumno_id):
    alumno = get_object_or_404(Perfil, id=alumno_id, rol='estudiante')
    
    if request.method == 'POST' and 'asignar_logro' in request.POST:
        nombre_logro = request.POST.get('nombre_logro')
        icono_logro = request.POST.get('icono_logro')
        descripcion_logro = request.POST.get('descripcion_logro')
        
        if nombre_logro and icono_logro:
            Logro.objects.create(
                usuario=alumno.user,
                nombre=nombre_logro,
                icono=icono_logro,
                descripcion=descripcion_logro or "Asignado por el profesor."
            )
            messages.success(request, f'¡Medalla "{nombre_logro}" asignada con éxito a {alumno.user.username}! 🏆')
            return redirect('detalle_alumno', alumno_id=alumno_id)

    progreso = Progreso.objects.filter(usuario=alumno.user).order_by('-fecha_creacion')
    logros = Logro.objects.filter(usuario=alumno.user).order_by('-id')
    
    context = {
        'alumno': alumno,
        'progreso': progreso,
        'logros': logros,
    }
    return render(request, 'teacher/detalle_alumno.html', context)

@csrf_exempt 
@login_required
def gestionar_actividades(request):
    nombres_correctos = [
        'Vocales', 'Matemáticas', 'Colores', 'Animales', 
        'Familia', 'Valores', 'Cuerpo', 'Memoria',
        'Mercadito', 'Unir', 'Plana'
    ]
    
    for nombre in nombres_correctos:
        try:
            if not ConfiguracionActividad.objects.filter(nombre=nombre).exists():
                ConfiguracionActividad.objects.create(
                    nombre=nombre, 
                    esta_activa=True,
                    slug=nombre.lower().replace('á', 'a').replace('é', 'e')
                )
        except Exception:
            pass

    if request.method == 'POST':
        actividad_id = request.POST.get('actividad_id')
        esta_activa_str = request.POST.get('esta_activa')

        if actividad_id:
            actividad = get_object_or_404(ConfiguracionActividad, id=actividad_id)

            if esta_activa_str is not None:
                actividad.esta_activa = (esta_activa_str == 'true')
            else:
                actividad.esta_activa = not actividad.esta_activa

            actividad.save()

            if request.headers.get('x-requested-with') == 'XMLHttpRequest' or esta_activa_str is not None:
                from django.http import JsonResponse
                return JsonResponse({'status': 'ok', 'esta_activa': actividad.esta_activa})

        return redirect('gestionar_actividades')

    actividades = ConfiguracionActividad.objects.all().order_by('nombre')
    return render(request, 'teacher/activities.html', {'actividades': activities})

@login_required
def menu_juegos(request):
    juegos_permitidos = ConfiguracionActividad.objects.filter(esta_activa=True)
    return render(request, 'estudiante/menu.html', {'juegos': juegos_permitidos})

@login_required
def student_dashboard(request):
    progreso = Progreso.objects.filter(usuario=request.user).count() 
    puntaje = Progreso.objects.filter(usuario=request.user).aggregate(total=Sum('puntaje'))['total'] or 0
    logros = Logro.objects.filter(usuario=request.user).count()
    juegos_activos = ConfiguracionActividad.objects.filter(esta_activa=True)

    context = {
        'progreso': progreso,  
        'puntaje': puntaje, 
        'logros': logros, 
        'juegos': juegos_activos 
    }
    return render(request, 'student/dashboard.html', context)

def sincronizar_juegos_db():
    from .models import ConfiguracionActividad
    nombres_requeridos = [
        'Vocales', 'Matemáticas', 'Colores', 'Animales', 
        'Familia', 'Valores', 'Cuerpo', 'Memoria',
        'Mercadito', 'Unir', 'Plana'
    ]
    for nombre in nombres_requeridos:
        ConfiguracionActividad.objects.get_or_create(nombre=nombre)

@login_required
def canciones_list(request):
    return render(request, 'student/songs_list.html', {'canciones': MODULES_CANCIONES.values()})

@login_required
def canciones_detail(request, cancion_id):
    cancion = MODULES_CANCIONES.get(cancion_id)
    return render(request, 'student/songs_detail.html', {'cancion': cancion})

def cuento_detail(request, cuento_id):
    cuento = get_object_or_404(Cuento, id=cuento_id)
    return render(request, 'student/story_detail.html', {'cuento': cuento})

def cuentos_list(request):
    cuentos = Cuento.objects.all() 
    return render(request, 'student/story_list.html', {'cuentos': cuentos})

@login_required
def mercadito_view(request):
    if not require_role(request.user, ['estudiante', 'profesor', 'admin']):
        return HttpResponseForbidden('Acceso denegado.')
        
    if not ConfiguracionActividad.objects.filter(nombre='Mercadito', esta_activa=True).exists() and not request.user.is_superuser:
        messages.error(request, 'El Mercadito está cerrado por el profesor en este momento. 🔒')
        return redirect('student_dashboard')

    return render(request, 'student/market.html')

@login_required
def game_match(request):
    if not require_role(request.user, ['estudiante', 'profesor', 'admin']):
        return HttpResponseForbidden('Acceso denegado.')
        
    if not ConfiguracionActividad.objects.filter(nombre='Unir', esta_activa=True).exists() and not request.user.is_superuser:
        messages.error(request, 'El juego de Unir Parejas está cerrado por el profesor. 🔒')
        return redirect('student_dashboard')

    return render(request, 'student/game_match.html')

@login_required
def configuracion_view(request):
    form_password = PasswordChangeForm(request.user)

    if request.method == 'POST':
        if 'guardar_perfil' in request.POST:
            nuevo_email = request.POST.get('email')
            request.user.email = nuevo_email
            request.user.save()
            messages.success(request, '¡Perfil actualizado correctamente! 🌟')
            return redirect('configuracion')

        elif 'cambiar_password' in request.POST:
            form_password = PasswordChangeForm(request.user, request.POST)
            if form_password.is_valid():
                user = form_password.save()
                update_session_auth_hash(request, user)
                messages.success(request, '¡Tu contraseña ha sido cambiada! 🔐')
                return redirect('configuracion')
            else:
                messages.error(request, 'Hubo un error. Por favor verifica los datos.')

    return render(request, 'teacher/configuracion.html', {
        'form_password': form_password
    })

@login_required
def game_planas(request):
    if not require_role(request.user, ['estudiante', 'profesor', 'admin']):
        return HttpResponseForbidden('Acceso denegado.')
        
    if not ConfiguracionActividad.objects.filter(nombre='Plana', esta_activa=True).exists() and not request.user.is_superuser:
        messages.error(request, 'El juego de Planas de Escritura está cerrado por el profesor. 🔒')
        return redirect('student_dashboard')

    return render(request, 'student/game_planas.html')

@login_required
def student_module(request, tipo):
    module = MODULES.get(tipo)
    if not module:
        raise Http404("El módulo no existe")
    
    mapeo_seguridad = {
        'vocales': 'Vocales',
        'numeros': 'Matemáticas',
        'colores': 'Colores',
        'animales': 'Animales',
        'familia': 'Familia',
        'valores': 'Valores',
        'cuerpo': 'Cuerpo'
    }
    
    nombre_db = mapeo_seguridad.get(tipo)
    if nombre_db and not request.user.is_superuser and not request.user.username.lower().startswith('profe'):
        if not ConfiguracionActividad.objects.filter(nombre=nombre_db, esta_activa=True).exists():
            messages.error(request, f'El módulo de {module["title"]} está bloqueado por el profesor. 🔒')
            return redirect('student_dashboard')

    context = {
        'module': module, 
        'tipo': tipo
    }
    
    if tipo == 'cuerpo':
        video_id = "UDNJ8SvT8Dw"
        context['video_url'] = f"https://www.youtube-nocookie.com/embed/{video_id}?autoplay=0&rel=0&origin=http://127.0.0.1:8000"
    
    return render(request, 'student/module.html', context)