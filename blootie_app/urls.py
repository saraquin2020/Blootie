from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('redirigir/', views.redirect_by_role, name='redirect_by_role'),
    

    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/usuarios/', views.admin_users, name='admin_users'),
    path('admin-panel/actividades/', views.admin_activities, name='admin_activities'),

    path('profesor-panel/', views.teacher_dashboard, name='teacher_dashboard'),
    path('profesor-panel/estudiantes/', views.teacher_students, name='teacher_students'),
    path('profesor-panel/actividades/', views.teacher_activities, name='teacher_activities'),

    path('estudiante-panel/', views.student_dashboard, name='student_dashboard'),
    path('estudiante-panel/modulo/<str:tipo>/', views.student_module, name='student_module'),
    path('estudiante-panel/memoria/', views.student_memory, name='student_memory'),
    path('estudiante-panel/logros/', views.student_achievements, name='student_achievements'),

    # --- RUTAS DE LOS JUEGOS ---
    path('juego/vocales/', views.game_bubbles, name='game_bubbles'),
    path('juego/numeros/', views.game_numbers, name='game_numbers'),
    path('juego/colores/', views.game_colors, name='game_colors'),
    path('juego/animales/', views.game_animals, name='game_animals'),
    path('juego/familia/', views.game_family, name='game_family'),
    path('juego/valores/', views.game_values, name='game_values'),
    path('juego/cuerpo/', views.game_body, name='game_body'),
    path('juego/planas/', views.game_planas, name='game_planas'),

    path('registrar/', views.register, name='register'),
    # Cambia 'teacher_panel' por 'dashboard'
    path('teacher-panel/', views.teacher_panel, name='dashboard'),
    path('mis-alumnos/', views.lista_alumnos, name='lista_alumnos'),   

    path('alumno/<int:alumno_id>/', views.detalle_alumno, name='detalle_alumno'),
    # urls.py
    path('juegos/', views.menu_juegos, name='menu_juegos'),
   path('gestionar-actividades/', views.gestionar_actividades, name='gestionar_actividades'),

   path('canciones/', views.canciones_list, name='songs_list'),
    path('canciones/<str:cancion_id>/', views.canciones_detail, name='songs_detail'),

    path('cuentos/', views.cuentos_list, name='student_stories'),
    path('cuentos/<int:cuento_id>/', views.cuento_detail, name='story_detail'),    
    
    path('mercadito/', views.mercadito_view, name='mercadito'),
    path('juego-unir/', views.game_match, name='game_match'),

    path('configuracion/', views.configuracion_view, name='configuracion'),

]