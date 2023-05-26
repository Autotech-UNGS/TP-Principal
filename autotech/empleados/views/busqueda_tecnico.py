import requests
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from .validadores_views import ValidadorDatosEmpleado
from empleados.api_client.client_tecnico import ClientTecnicos


class TecnicoViewSet(ViewSet):
    validador_empleado = ValidadorDatosEmpleado()

    @action(detail=False, methods=['get'])
    def lista_tecnicos(self, request):
        taller_sup = request.GET.get('branch')

        if not self.validador_empleado.taller(taller_sup):
            return HttpResponse('error: numero de taller no valido', status=400)
        
        tecnicos =ClientTecnicos.obtener_datos_especificos_tecnicos(taller_sup)    
        return JsonResponse({'tecnicos': tecnicos})

    @action(detail=False, methods=['get'])
    def categorias(self, request):
        """Devuelve una lista de todas las categorías de técnico disponibles.
        """
        tipos_categorias = ["A", "B", "C", "D"]
        return JsonResponse(tipos_categorias, safe=False)

    @action(detail=False, methods=['get'])
    def filtrar_tecnicos(self, request):
        taller_sup= request.GET.get('branch')
        categoria_tec= request.GET.get('categoria')
        dni_tec = request.GET.get('dni')
        nombre_tec = request.GET.get('nombre_completo')
        
        if not self.validador_empleado.taller(taller_sup):
            return HttpResponse('error: numero de taller no valido', status=400)
        if not self.validador_empleado.categoria_tecnico(categoria=categoria_tec):
            return HttpResponse('error: categoría no valida', status=400)
        if not self.validador_empleado.dni(dni=dni_tec):
            return HttpResponse('error: DNI no valido', status=400)
        
        try:
            tecnicos = self.obtener_tecnicos(taller_sup, categoria_tec, dni_tec, nombre_tec)
            return JsonResponse({'tecnicos': tecnicos})
        except requests.HTTPError as e:
            return HttpResponse(str(e), status=e.response.status_code)
    
    def obtener_tecnicos(self, taller_sup, categoria_tec=None, dni_tec=None, nombre_tec=None):   
        tecnicos = ClientTecnicos.obtener_datos_especificos_tecnicos(taller_sup)
        
        if categoria_tec is not None:
            tecnicos = [tecnico for tecnico in tecnicos if tecnico['categoria'] == categoria_tec]
        if dni_tec is not None:
            tecnicos = [tecnico for tecnico in tecnicos if tecnico['dni'] == dni_tec]  
        if nombre_tec is not None:
            tecnicos = [tecnico for tecnico in tecnicos if nombre_tec.lower() in tecnico['nombre_completo'].lower()]
        if not tecnicos:
            return []
        
        return tecnicos
    

