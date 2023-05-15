from rest_framework import routers
from .views import RegistroEvaluacionAdminCreateViewSet, RegistroEvaluacionAdminReadOnlyViewSet,  IdTaskPuntajeCreateView, RegistroEvaluacionReadOnlyView

router = routers.DefaultRouter()

router.register(r'registros-admin', RegistroEvaluacionAdminReadOnlyViewSet, basename='registros_evaluaciones')
router.register(r'registros-crear-admin', RegistroEvaluacionAdminCreateViewSet, basename='crear_registro_evaluacion_admin')

router.register(r'registros',RegistroEvaluacionReadOnlyView , basename= 'crear-registro-evaluacion')


urlpatterns = router.urls

