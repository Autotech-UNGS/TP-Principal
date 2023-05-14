from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('administracion.urls')),
    path('tecnicos/', include('tecnico.urls')),
    path('turnos/', include('turnos.urls'))
]
