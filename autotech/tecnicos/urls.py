from django.urls import path
from . import views


urlpatterns = [
    path('listar/', views.TecnicoViewSet.as_view({'get': 'lista_tecnicos'}), name='lista-tecnicos'),
    path('detalle/<int:id_tecnico>/', views.TecnicoViewSet.as_view({'get': 'detalle_trabajos_tecnico'}), name='detalle-trabajos-tecnico'),
    path('categorias/', views.TecnicoViewSet.as_view({'get': 'categorias'}), name='categorias'),
    path('filtro/', views.TecnicoViewSet.as_view({'get': 'filtrar_tecnicos'}), name='filtrar-tecnicos'),
    path('trabajos-en-proceso/<int:id_tecnico>/', views.TecnicoViewSet.as_view({'get': 'trabajos_en_proceso_tecnico'}), name='trabajos-en-proceso'),
    path('trabajos-terminados/<int:id_tecnico>/', views.TecnicoViewSet.as_view({'get': 'trabajos_terminados_tecnico'}), name='trabajos-terminados')
]