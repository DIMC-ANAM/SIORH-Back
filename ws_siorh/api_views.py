from rest_framework import filters, pagination, viewsets

from .models import BajasFin, PlantillaFin
from .serializers import BajasFinSerializer, PlantillaFinSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
import re
import unicodedata


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
        'estado_nomina',
        'posicion',
        'nivel',
        'num_empleado',
        'rfc',
        'nombre_puesto_funcional',
        'dg_o_aduana_compactada',
        'programa',
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
            'departamento':                    'departamento__icontains',
            'tipo_de_contratacion':            'tipo_de_contratacion__icontains',
            'tipo_de_personal_sedena_semar':   'tipo_de_personal_sedena_semar__icontains',
            'rango':                           'rango__icontains',
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


@api_view(['GET'])
def aduana_tablero(request):
    """Devuelve un resumen por aduana (dg_o_aduana_compactada) con conteos
    de civiles y militares y la suma del COSTO_PLAZA_ANUAL.
    """
    qs = PlantillaFin.objects.values(
        'dg_o_aduana_compactada',
        'personal_militar_o_civil',
        'costo_plaza_anual',
        'nombres',
        'depuracion_vacancia',
        'posicion',
        'reportada',
        'nombre_puesto_funcional',
        'posicion_civil_sedena_semar',
    )

    def parse_cost(val):
        if not val:
            return 0.0
        # Eliminar símbolos no numéricos (comas, signos de moneda, espacios)
        cleaned = re.sub(r"[^0-9\-\.]+", '', str(val))
        try:
            return float(cleaned) if cleaned else 0.0
        except Exception:
            return 0.0

    def es_vacante(row):
        # Usar una regex con límites de palabra para evitar falsos positivos
        pattern = re.compile(r"\b(vacante|vacantes|vacancia|vacío|vacio|vacía|sin ocupar)\b", re.IGNORECASE)

        check_fields = [
            row.get('nombres'),
            row.get('depuracion_vacancia'),
            row.get('posicion'),
            row.get('reportada'),
            row.get('nombre_puesto_funcional'),
            row.get('posicion_civil_sedena_semar'),
            row.get('personal_militar_o_civil'),
        ]

        for v in check_fields:
            if not v:
                continue
            if pattern.search(str(v)):
                return True

        return False

    result = {}
    for row in qs:
        if es_vacante(row):
            continue

        raw_aduana = row.get('dg_o_aduana_compactada') or ''
        aduana_trim = str(raw_aduana).strip()

        def _normalize_no_diacritic(s: str) -> str:
            s = s or ''
            s = str(s)
            s = unicodedata.normalize('NFKD', s)
            s = ''.join(ch for ch in s if not unicodedata.combining(ch))
            return s.strip().lower()

        aduana_norm = _normalize_no_diacritic(aduana_trim)

        # Unir DOAF CDMX y DOAF Queretaro con ANAM
        if aduana_norm in ('doaf cdmx', 'doaf cdmx ', 'doaf queretaro', 'doaf queretaro ', 'anam'):
            aduana = 'ANAM'
        else:
            aduana = aduana_trim or 'SIN ADUANA'
        tipo = (row.get('personal_militar_o_civil') or '').strip()
        costo = parse_cost(row.get('costo_plaza_anual'))

        entry = result.setdefault(
            aduana,
            {
                'aduana': aduana,
                'civiles': 0,
                'militares': 0,
                'costo_plaza_anual_total': 0.0,
                'costo_civiles': 0.0,
                'costo_militares': 0.0,
            },
        )

        # Contabilizar según el texto en 'personal_militar_o_civil'
        lower = tipo.lower()
        if 'militar' in lower or 'sedena' in lower or 'semar' in lower:
            entry['militares'] += 1
            entry['costo_militares'] += costo
        else:
            # Por defecto considerar como civil si no contiene 'militar'
            entry['civiles'] += 1
            entry['costo_civiles'] += costo

        entry['costo_plaza_anual_total'] += costo

    # Convertir a lista y ordenar por nombre de aduana
    data = sorted(result.values(), key=lambda x: x['aduana'] or '')

    # Asegurar tipos JSON serializables (floats)
    for e in data:
        e['costo_plaza_anual_total'] = round(e.get('costo_plaza_anual_total', 0.0), 2)
        e['costo_civiles'] = round(e.get('costo_civiles', 0.0), 2)
        e['costo_militares'] = round(e.get('costo_militares', 0.0), 2)

    return Response(data)
