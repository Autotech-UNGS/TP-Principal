from django.urls import path
from .views import busqueda_tecnico, trabajos_tecnico


urlpatterns = [
    path('listar/', busqueda_tecnico.TecnicoViewSet.as_view({'get': 'lista_tecnicos'}), name='lista-tecnicos'),
    path('categorias/', busqueda_tecnico.TecnicoViewSet.as_view({'get': 'categorias'}), name='categorias'),
    path('filtro/', busqueda_tecnico.TecnicoViewSet.as_view({'get': 'filtrar_tecnicos'}), name='filtrar-tecnicos'),
   
    path('detalle/<int:id_tecnico>/', trabajos_tecnico.TrabajosTecnicoViewSet.as_view({'get': 'detalle_trabajos_tecnico'}), name='detalle-trabajos-tecnico'),
    path('trabajos-en-proceso/<int:id_tecnico>/', trabajos_tecnico.TrabajosTecnicoViewSet.as_view({'get': 'trabajos_en_proceso_tecnico'}), name='trabajos-en-proceso'),
    path('trabajos-terminados/<int:id_tecnico>/', trabajos_tecnico.TrabajosTecnicoViewSet.as_view({'get': 'trabajos_terminados_tecnico'}), name='trabajos-terminados'),
    path('trabajos-en-proceso-evaluacion/<int:id_tecnico>/', trabajos_tecnico.TrabajosTecnicoViewSet.as_view({'get': 'trabajos_en_proceso_evaluacion_tecnico'}), name='trabajos-en-proceso-evaluacion'),
    path('trabajos-en-proceso-service/<int:id_tecnico>/', trabajos_tecnico.TrabajosTecnicoViewSet.as_view({'get': 'trabajos_en_proceso_service_tecnico'}), name='trabajos-en-proceso-service'),
    path('trabajos-en-proceso-reparacion/<int:id_tecnico>/', trabajos_tecnico.TrabajosTecnicoViewSet.as_view({'get': 'trabajos_en_proceso_reparacion_tecnico'}), name='trabajos-en-proceso-reparacion'),
    path('trabajos-en-proceso-extraordinario/<int:id_tecnico>/', trabajos_tecnico.TrabajosTecnicoViewSet.as_view({'get': 'trabajos_en_proceso_extraordinario_tecnico'}), name='trabajos-en-proceso-extraordinario'),
]