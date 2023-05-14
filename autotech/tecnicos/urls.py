from django.urls import path
from . import views


urlpatterns = [
    path('tecnicos/', views.TecnicoViewSet.as_view({'get': 'lista_tecnicos'}), name='lista_tecnicos'),
    path('tecnico/<int:pk>/', views.TecnicoViewSet.as_view({'get': 'detalle_trabajos_tecnico'}), name='detalle_trabajos_tecnico'),
    path('categorias/', views.TecnicoViewSet.as_view({'get': 'categorias'}), name='categorias'),
    path('filtro/', views.TecnicoViewSet.as_view({'get': 'filtrar_tecnicos'}), name='filtrar_tecnicos'),
]