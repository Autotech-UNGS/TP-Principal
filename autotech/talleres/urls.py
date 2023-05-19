from django.urls import path
from . import views

urlpatterns = [
    path('talleres-list/', views.VisualizarTalleresViewSet.as_view({'get':'talleresList'}), name='talleres-list'),
    path('talleres-detalle/<int:id_taller>/', views.VisualizarTalleresViewSet.as_view({'get':'talleresDetalle'}), name='talleres-detalle')
]