from django.urls import path
from .views import verificar_modificar_garantias

urlpatterns = [
    path('garantia-vigente/<str:patente>/<str:fecha_turno>/<int:service_solicitado>/', verificar_modificar_garantias.VerificarEstadoGarantia.as_view({'get': 'garantia_vigente'}), name='mantiene-garantia'),
    path('estado-garantia/<str:patente>/', verificar_modificar_garantias.VerificarEstadoGarantia.as_view({'get': 'estado_garantia'}), name='estado-garantia')
]