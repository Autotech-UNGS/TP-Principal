from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('administracion.urls')),
    # path('buscar_tecnicos/', include('busquedatecnicos.urls')),
    path('',include('busquedatecnicos.urls')),
]
#comentario random para subir la rama joaco