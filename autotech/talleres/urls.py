from django.urls import path
from .views import visualizar_talleres, alta_talleres, visualizar_sucursales, modificar_talleres, reasignar_taller

urlpatterns = [
    path('crear/', alta_talleres.TalleresCreate.as_view(), name = 'talleres-crear'),
    
    path('talleres-list/', visualizar_talleres.VisualizarTalleresViewSet.as_view({'get':'talleresList'}), name='talleres-list'),
    path('list-activos/', visualizar_talleres.VisualizarTalleresViewSet.as_view({'get':'talleresActivosList'}), name='talleres-activos-list'),
    path('talleres-detalle/<int:id_taller>/', visualizar_talleres.VisualizarTalleresViewSet.as_view({'get':'talleresDetalle'}), name='talleres-detalle'),
    
    path('modificar/<int:id_taller>/', modificar_talleres.ModificarTaller.as_view(), name = 'talleres-modificar'),
    path('reasignar/', reasignar_taller.ReasignarTaller.as_view(), name = 'reasignar-taller'),
    path('actualizar/<int:id_sucursal>/', modificar_talleres.ActualizarTallerAdmin.as_view(), name = 'actualizar-taller'),
    path('cambiar-estado/<int:id_taller>/', modificar_talleres.ActualizarEstado.as_view(), name = 'cambiar-estado-taller'),
    path('existe/<int:id_sucursal>/', visualizar_sucursales.SucursalTieneTaller.as_view(), name = 'sucursal-tiene-taller'),

    path('sucursales-validas-activas/', visualizar_sucursales.VisualizarSucursalesConTallerValidas.as_view(), name = 'sucursales-list'),
    path('sucursales-validas-activas/<int:id_sucursal>/', visualizar_sucursales.VisualizarUnaSucursalConTallerValida.as_view(), name = 'sucursales-list-una'),
    path('sucursales-sin-taller/', visualizar_sucursales.VisualizarSucursalesSinTaller.as_view(), name = 'sucursales-list-sin-taller'),

    

]