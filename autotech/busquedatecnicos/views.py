import requests
from django.http import JsonResponse, HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from administracion.models import Turno_taller
from .validaciones_views import ValidadorDatosTecnico


class TecnicoViewSet(ViewSet):
    validador = ValidadorDatosTecnico()

    @action(detail=False, methods=['get'])
    def lista_tecnicos(self, request):
        sucursal_supervisor = request.GET.get('branch')     
        if not self.validador.sucursal(sucursal_supervisor):
            return HttpResponse({'message' : 'error: el numero de sucursal no es valido'}, status=400)
        tecnicos = self.tecnicos_todos(sucursal_supervisor)
        return JsonResponse({'tecnicos': tecnicos})

    @action(detail=True, methods=['get'])
    def detalle_trabajos_tecnico(self, request, pk):
        sucursal_supervisor = request.GET.get('branch')       
        if not self.validador.sucursal(sucursal_supervisor):
            return HttpResponse({'message' : 'error: el numero de sucursal no es valido'}, status=400)      
        id_taller_sucursal = "T" + sucursal_supervisor[-3:]
        turnos = Turno_taller.objects.filter(tecnico_id=pk, taller_id=id_taller_sucursal).order_by('estado')
        data = []
        for turno in turnos:
            data.append({
                "id_turno": turno.id_turno,
                "patente": turno.patente,
                "fecha_inicio": turno.fecha_inicio,
                "hora_inicio": turno.hora_inicio,
                "fecha_fin": turno.fecha_fin,
                "hora_fin": turno.hora_fin,
                "tipo": turno.tipo,
                "estado": turno.estado
            })
        return Response(data)

    @action(detail=False, methods=['get'])
    def categorias(self, request):
        """Devuelve una lista de todas las categorías de técnico disponibles.
        """
        tipos_categorias = ["A", "B", "C", "D"]
        return JsonResponse(tipos_categorias, safe=False)

    @action(detail=False, methods=['get'])
    def filtrar_tecnicos(self, request):
        sucursal_supervisor = request.GET.get('branch')
        categoria = request.GET.get('categoria')
        dni = request.GET.get('dni')
        nombre = request.GET.get('nombre_completo')
        if not self.validador.sucursal(sucursal_supervisor):
            return HttpResponse({'message' : 'Sucursal no valida'}, status=400)
        if not self.validador.categoria(categoria=categoria):
            return HttpResponse({'message' : 'Categoría no válida'}, status=400)
        if not self.validador.dni(dni=dni):
            return HttpResponse({'message' : 'DNI no válida'}, status=400)
        try:
            tecnicos = self.obtener_tecnicos(sucursal_supervisor, categoria, dni, nombre)
            return JsonResponse({'tecnicos': tecnicos})
        except requests.HTTPError as e:
            return HttpResponse({'message': str(e)}, status=e.response.status_code)
    
    def obtener_tecnicos(self, sucursal_supervisor, categoria=None, dni=None, nombre=None):
        tecnicos = self.tecnicos_todos(sucursal_supervisor)
        if categoria is not None:
            tecnicos = [tecnico for tecnico in tecnicos if tecnico['categoria'] == categoria]
        if dni is not None:
            tecnicos = [tecnico for tecnico in tecnicos if tecnico['dni'] == dni]  
        if nombre is not None:
            tecnicos = [tecnico for tecnico in tecnicos if nombre.lower() in tecnico['nombre_completo'].lower()]
        if not tecnicos:
            return []
        return tecnicos
    
    @staticmethod
    def tecnicos_todos(sucursal_supervisor):
        url = "https://api-rest-pp1.onrender.com/api/usuarios/"
        usuarios_data = requests.get(url)
        if usuarios_data.status_code != 200:
            raise requests.HTTPError({'message error' : usuarios_data.status_code})
        usuarios_data = usuarios_data.json()
        tecnicos = [{
            'id_empleado': tecnico['id_empleado'],
            'nombre_completo': tecnico['nombre_completo'], 
            'dni': tecnico['dni'], 
            'categoria': tecnico['categoria'], 
            'branch': tecnico['branch']
            } for tecnico in usuarios_data if tecnico['branch'].endswith(sucursal_supervisor[-3:]) and tecnico['tipo'] == "Tecnico"]   
        return tecnicos


