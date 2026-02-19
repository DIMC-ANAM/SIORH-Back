from rest_framework import filters, pagination, viewsets

from .models import BajasFin, PlantillaFin
from .serializers import BajasFinSerializer, PlantillaFinSerializer


class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 200


class PlantillaFinViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PlantillaFinSerializer
    pagination_class = StandardResultsSetPagination
    lookup_field = 'posicion'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        'nombres',
        'curp',
        'rfc',
        'num_empleado',
        'posicion',
    ]
    ordering_fields = ['nombres', 'smn', 'nivel', 'estado_nomina', 'programa']
    ordering = ['-smn']

    def get_queryset(self):
        queryset = PlantillaFin.objects.all()
        params = self.request.query_params

        map_filters = {
            'nombres':                 'nombres__icontains',
            'rfc':                     'rfc__icontains',
            'num_empleado':            'num_empleado__icontains',
            'posicion':                'posicion__icontains',
            'curp':                    'curp__icontains',
            'nivel':                   'nivel__icontains',
            'motivo':                  'motivo__icontains',
            'qna':                     'qna__icontains',
            'estado_nomina':           'estado_nomina__icontains',
            'programa':                'programa__icontains',
            'nombre_puesto_funcional': 'nombre_puesto_funcional__icontains',
            'unidad_administrativa':   'unidad_administrativa__icontains',
            'dg_o_aduana_compactada':  'dg_o_aduana_compactada__icontains',
            'departamento':            'departamento__icontains',
            'tipo_de_contratacion':    'tipo_de_contratacion__icontains',
        }

        for param_name, orm_filter in map_filters.items():
            value = params.get(param_name)
            if value:
                queryset = queryset.filter(**{orm_filter: value})

        return queryset


class BajasFinViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = BajasFinSerializer
    pagination_class = StandardResultsSetPagination
    lookup_field = 'id_empleado'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombre', 'rfc', 'id_empleado', 'motivo', 'puesto_funcional', 'nivel']
    ordering_fields = ['nombre', 'fecha_de_captura', 'motivo', 'nivel']
    ordering = ['-fecha_de_captura']

    def get_queryset(self):
        queryset = BajasFin.objects.all()
        params = self.request.query_params

        map_filters = {
            'motivo': 'motivo__icontains',
            'nivel': 'nivel__icontains',
            'unidad_administrativa': 'unidad_administrativa__icontains',
            'posicion': 'posicion__icontains',
        }

        for param_name, orm_filter in map_filters.items():
            value = params.get(param_name)
            if value:
                queryset = queryset.filter(**{orm_filter: value})

        return queryset
