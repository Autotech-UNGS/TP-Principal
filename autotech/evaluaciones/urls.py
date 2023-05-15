from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers
from .views import RegistroEvaluacionXAdminCreate, RegistroEvaluacionXAdminReadOnly, RegistroEvaluacionCreate

router = routers.DefaultRouter()

router.register(r'registros-admin', RegistroEvaluacionXAdminReadOnly, basename='registros_evaluaciones')
router.register(r'registros-crear-admin', RegistroEvaluacionXAdminCreate, basename='crear_registro_evaluacion_para_admin')

urlpatterns = [
    path('registros/crear/', RegistroEvaluacionCreate.as_view(), name= 'crear_registro_evaluacion')
]

urlpatterns = format_suffix_patterns(urlpatterns)

urlpatterns += router.urls

