from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    #path('', include('administracion.urls')),
    path('', admin.site.urls),
    path('turnos/', include('turnos.urls')),
    path('evaluaciones/', include('evaluaciones.urls')),
    path('tecnicos/', include('tecnicos.urls'))
]
