from django.urls import path
from .views import visualizar_talleres, alta_talleres, visualizar_sucursales

urlpatterns = [
    path('talleres-list/', visualizar_talleres.VisualizarTalleresViewSet.as_view({'get':'talleresList'}), name='talleres-list'),
    path('talleres-detalle/<int:id_taller>/', visualizar_talleres.VisualizarTalleresViewSet.as_view({'get':'talleresDetalle'}), name='talleres-detalle'),
    path('crear/', alta_talleres.TalleresCreate.as_view(), name = 'talleres-crear'),
    path('sucursales-validas-activas/', visualizar_sucursales.VisualizarSucursalesConTallerValidas.as_view(), name = 'sucursales-list'),
    path('sucursales-validas-activas/<int:id_sucursal>', visualizar_sucursales.VisualizarUnaSucursalConTallerValida.as_view(), name = 'sucursales-una'),

]