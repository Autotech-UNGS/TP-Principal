from django.urls import path
from .views import visualizar_talleres, alta_talleres, visualizar_sucursales, modificar_talleres

urlpatterns = [
    path('talleres-list/', visualizar_talleres.VisualizarTalleresViewSet.as_view({'get':'talleresList'}), name='talleres-list'),
    path('talleres-detalle/<int:id_taller>/', visualizar_talleres.VisualizarTalleresViewSet.as_view({'get':'talleresDetalle'}), name='talleres-detalle'),
    path('crear/', alta_talleres.TalleresCreate.as_view(), name = 'talleres-crear'),
    path('modificar/<int:id_taller>/', modificar_talleres.ModificarTaller.as_view(), name = 'talleres-modificar'),
    path('sucursales-validas-activas/', visualizar_sucursales.VisualizarSucursalesConTallerValidas.as_view(), name = 'sucursales-list'),
    path('sucursales-validas-activas/<int:id_sucursal>/', visualizar_sucursales.VisualizarUnaSucursalConTallerValida.as_view(), name = 'sucursales-list-una'),
    path('sucursales-sin-taller/', visualizar_sucursales.VisualizarSucursalesSinTaller.as_view(), name = 'sucursales-list-sin-taller'),


]