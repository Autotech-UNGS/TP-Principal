from rest_framework import routers
from .views import TallerViewSet,TurnoTallerViewSet, ChecklistReparacionViewSet, RegistroReparacionViewSet

router = routers.DefaultRouter()
router.register(r'talleres_admin', TallerViewSet, 'talleres_admin')
router.register(r'turnos_admin', TurnoTallerViewSet , 'turnos_admin')
router.register(r'checklist_reparacion_admin', ChecklistReparacionViewSet , 'checklist_reparacion_admin')
router.register(r'registro_reparacion_admin', RegistroReparacionViewSet , 'registro_reparacion_admin')


urlpatterns = router.urls
