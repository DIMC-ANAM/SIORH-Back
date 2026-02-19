import base64

from rest_framework import serializers

from .models import BajasFin, PlantillaFin


class PlantillaFinSerializer(serializers.ModelSerializer):
    foto_base64 = serializers.SerializerMethodField()

    class Meta:
        model = PlantillaFin
        fields = [
            'posicion',
            'estado_nomina',
            'num_empleado',
            'rfc',
            'curp',
            'nombres',
            'motivo',
            'fecha_efectiva_personal',
            'fecha_de_captura',
            'qna',
            'nivel',
            'programa',
            'unidad_administrativa',
            'departamento',
            'nombre_puesto_funcional',
            'tipo_de_contratacion',
            'dg_o_aduana_compactada',
            'smn',
            'tipo_de_personal_sedena_semar',
            'rango',
            'foto_base64',
        ]

    def get_foto_base64(self, obj):
        include_foto = self.context.get('request') and self.context['request'].query_params.get('include_foto') == '1'
        if include_foto and obj.foto:
            return base64.b64encode(obj.foto).decode('utf-8')
        return None


class BajasFinSerializer(serializers.ModelSerializer):
    foto_base64 = serializers.SerializerMethodField()

    class Meta:
        model = BajasFin
        fields = [
            'id_empleado',
            'posicion',
            'estado_nomina',
            'rfc',
            'curp',
            'nombre',
            'motivo',
            'fecha_efectiva_personal',
            'fecha_de_captura',
            'qna',
            'nivel',
            'unidad_administrativa',
            'puesto_funcional',
            'foto_base64',
        ]

    def get_foto_base64(self, obj):
        include_foto = self.context.get('request') and self.context['request'].query_params.get('include_foto') == '1'
        if include_foto and obj.foto:
            return base64.b64encode(obj.foto).decode('utf-8')
        return None
