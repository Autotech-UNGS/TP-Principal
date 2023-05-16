from django.urls import path

from . import views

urlpatterns = [
    path('',views.turnosOverview,name='turnos'),

    path('turnos-list/', views.turnosList, name='turnos-list'),

    path('turnos-detalle/<int:id_turno>/', views.turnoDetalle, name='turnos-detalle'),

    path('turnos-create/', views.crearTurno, name="turnos-create"),

    path('turnos-update/<int:id_turno>/', views.turnoUpdate, name="turnos-update"),
    
    path('dias-horarios-disponibles/<int:taller_id>/', views.diasHorariosDisponibles, name="dias-horarios-disponibles"),
    
    path('tecnicos-disponibles/<int:_id_turno>/', views.tecnicos_disponibles, name="tecnicos-disponibles"),
    
    path('asignar-tecnico/<int:id_tecnico>/<int:_id_turno>/', views.asignar_tecnico, name="asignar-tecnico"),
]


