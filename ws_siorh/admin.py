import base64
from django.contrib import admin
from django.http import HttpResponse
from django.utils.html import format_html
from .models import PlantillaFin, BajasFin
from django.db.models import Count
import openpyxl
from openpyxl.drawing.image import Image
from io import BytesIO

# Importamos lo necesario para la bitácora
from auditoria.models import RegistroActividad
from auditoria.utils import log_user_view # Función de ayuda para registrar

# --- "FÁBRICA" DE FILTROS ---
def crear_filtro_conteo(nombre_campo, titulo_filtro):
    class CustomConteoFiltro(admin.SimpleListFilter):
        title = titulo_filtro
        parameter_name = nombre_campo
        def lookups(self, request, model_admin):
            qs = model_admin.get_queryset(request)
            counts = qs.values(self.parameter_name).annotate(count=Count('pk')).order_by('-count')
            return [(item[self.parameter_name], f"{item[self.parameter_name]} ({item['count']})") for item in counts if item[self.parameter_name] is not None]
        def queryset(self, request, queryset):
            if self.value():
                return queryset.filter(**{self.parameter_name: self.value()})
            return queryset
    return CustomConteoFiltro

# --- CLASE DE ADMIN PARA PlantillaFin ---
class PlantillaFinAdmin(admin.ModelAdmin):
    actions = ['exportar_a_excel_con_imagenes']

    list_display = (
        'colored_miniatura', 'colored_nombres', 'colored_rfc', 'colored_num_empleado',
        'colored_posicion', 'colored_nivel', 'colored_programa', 'colored_dg_o_aduana_compactada',
        'colored_unidad_administrativa', 'colored_departamento', 'colored_nombre_puesto_funcional',
        'colored_estado_nomina'
    )
    search_fields = ('nombres', 'estado_nomina', 'posicion','nivel', 'num_empleado', 'rfc','nombre_puesto_funcional','dg_o_aduana_compactada','programa')
    fieldsets = (
        ('Información Personal', { 'fields': ('mostrar_foto_de_base_de_datos','nombres', 'rfc', 'curp', 'num_empleado') }),
        ('Detalles del Puesto', { 'fields': ('posicion', 'estado_nomina', 'nivel', 'codigo_presupuestal', 'nombre_puesto_funcional', 'tipo_de_contratacion') }),
    )
    readonly_fields = ('mostrar_foto_de_base_de_datos',)
    
    # --- MÉTODOS PARA COLOREAR Y MOSTRAR FOTOS ---
    def _get_row_color(self, obj):
        if obj.programa == 'Sin Código' or obj.estado_nomina == 'Baja': return '#FFDDDD'
        elif obj.estado_nomina == 'Vacante' and 'H00' in str(obj.programa): return '#D4EDDA'
        return ''

    @admin.display(description='Foto')
    def colored_miniatura(self, obj):
        color = self._get_row_color(obj)
        content = self.mostrar_miniatura(obj)
        return format_html('<div style="width:100%; height:100%; background-color:{}; padding:1px; text-align:center;">{}</div>', color, content)

    @admin.display(description='Nombre Completo', ordering='nombres')
    def colored_nombres(self, obj):
        color = self._get_row_color(obj)
        return format_html('<div style="width:100%; height:100%; background-color:{}; padding:5px;">{}</div>', color, obj.nombres)

    @admin.display(description='RFC', ordering='rfc')
    def colored_rfc(self, obj):
        color = self._get_row_color(obj)
        return format_html('<div style="width:100%; height:100%; background-color:{}; padding:5px;">{}</div>', color, obj.rfc)

    @admin.display(description='Num Empleado', ordering='num_empleado')
    def colored_num_empleado(self, obj):
        color = self._get_row_color(obj)
        return format_html('<div style="width:100%; height:100%; background-color:{}; padding:5px;">{}</div>', color, obj.num_empleado)

    @admin.display(description='Posición', ordering='posicion')
    def colored_posicion(self, obj):
        color = self._get_row_color(obj)
        return format_html('<div style="width:100%; height:100%; background-color:{}; padding:5px;">{}</div>', color, obj.posicion)

    @admin.display(description='Nivel', ordering='nivel')
    def colored_nivel(self, obj):
        color = self._get_row_color(obj)
        return format_html('<div style="width:100%; height:100%; background-color:{}; padding:5px;">{}</div>', color, obj.nivel)

    @admin.display(description='Programa', ordering='programa')
    def colored_programa(self, obj):
        color = self._get_row_color(obj)
        return format_html('<div style="width:100%; height:100%; background-color:{}; padding:5px;">{}</div>', color, obj.programa)
        
    @admin.display(description='DG o Aduana', ordering='dg_o_aduana_compactada')
    def colored_dg_o_aduana_compactada(self, obj):
        color = self._get_row_color(obj)
        return format_html('<div style="width:100%; height:100%; background-color:{}; padding:5px;">{}</div>', color, obj.dg_o_aduana_compactada)

    @admin.display(description='Unidad Admin.', ordering='unidad_administrativa')
    def colored_unidad_administrativa(self, obj):
        color = self._get_row_color(obj)
        return format_html('<div style="width:100%; height:100%; background-color:{}; padding:5px;">{}</div>', color, obj.unidad_administrativa)

    @admin.display(description='Departamento', ordering='departamento')
    def colored_departamento(self, obj):
        color = self._get_row_color(obj)
        return format_html('<div style="width:100%; height:100%; background-color:{}; padding:5px;">{}</div>', color, obj.departamento)

    @admin.display(description='Puesto Funcional', ordering='nombre_puesto_funcional')
    def colored_nombre_puesto_funcional(self, obj):
        color = self._get_row_color(obj)
        return format_html('<div style="width:100%; height:100%; background-color:{}; padding:5px;">{}</div>', color, obj.nombre_puesto_funcional)

    @admin.display(description='Estado Nómina', ordering='estado_nomina')
    def colored_estado_nomina(self, obj):
        color = self._get_row_color(obj)
        return format_html('<div style="width:100%; height:100%; background-color:{}; padding:5px;">{}</div>', color, obj.estado_nomina)

    def mostrar_foto_de_base_de_datos(self, obj):
        if obj.foto:
            imagen_base64 = base64.b64encode(obj.foto).decode('utf-8')
            return format_html(f'<img src="data:image/jpeg;base64,{imagen_base64}" style="max-width: 200px; height: auto;" />')
        return "No hay imagen en la base de datos."
    mostrar_foto_de_base_de_datos.short_description = 'Fotografía'

    def mostrar_miniatura(self, obj):
        if obj.foto:
            imagen_base64 = base64.b64encode(obj.foto).decode('utf-8')
            return format_html(f'<img src="data:image/jpeg;base64,{imagen_base64}" style="width: 60px; height: auto;" />')
        return "N/A"

    # --- ACCIÓN DE EXPORTAR CON REGISTRO EN BITÁCORA ---
    @admin.action(description="Exportar a Excel con Imágenes")
    def exportar_a_excel_con_imagenes(self, request, queryset):
        RegistroActividad.objects.create(usuario=request.user, tipo_accion='export', detalles=f"Exportó a Excel {queryset.count()} registros de Plantilla de Personal.")
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "Plantilla de Personal"
        headers = ['Posición', 'Nombre', 'RFC', 'SMN', 'Foto']
        sheet.append(headers)
        for registro in queryset:
            if registro.foto:
                try:
                    image_stream = BytesIO(registro.foto)
                    img = Image(image_stream)
                    proporcion = img.width / img.height
                    img.height = 80
                    img.width = 80 * proporcion
                except Exception: img = None
            else: img = None
            row_data = [registro.posicion, registro.nombres, registro.rfc, getattr(registro, 'smn', ''), '']
            sheet.append(row_data)
            if img:
                row_num = sheet.max_row
                sheet.add_image(img, f'E{row_num}')
                sheet.row_dimensions[row_num].height = 65
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="plantilla_personal.xlsx"'
        workbook.save(response)
        return response

    # --- REGISTRO DE CONSULTAS Y BÚSQUEDAS ---
    def changelist_view(self, request, extra_context=None):
        search_term = request.GET.get('q', '') 
        if search_term:
            log_user_view(request, f"Buscó '{search_term}' en Plantilla de Personal.", include_filters=False) # No incluir filtros si es búsqueda
        else:
            log_user_view(request, "Consultó la lista de Plantilla de Personal.", include_filters=True) # Incluir filtros si es consulta normal
        return super().changelist_view(request, extra_context)

    # --- REGISTRO DE VISTA DE DETALLE ---
    def change_view(self, request, object_id, form_url='', extra_context=None):
        try:
            obj = self.get_object(request, object_id)
            log_user_view(request, f"Consultó el detalle de Plantilla: {obj}", include_filters=False) # No incluir filtros aquí
        except Exception: 
            log_user_view(request, f"Intentó consultar detalle de Plantilla ID: {object_id}", include_filters=False)
        return super().change_view(request, object_id, form_url, extra_context)
        
    # --- GESTIÓN DE ACCIONES Y PERMISOS ---
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions: del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False

    class Media:
        css = { 'all': ('core/css/admin_sticky_headers.css',) }

# --- CLASE DE ADMIN PARA BajasFin ---
class BajasFinAdmin(admin.ModelAdmin):
    actions = ['exportar_a_excel_con_imagenes']
    list_display = ('mostrar_miniatura','nombre', 'rfc','id_empleado', 'posicion','nivel','motivo', 'fecha_efectiva_personal', 'puesto_funcional','unidad_administrativa')
    search_fields = ('nombre', 'id_empleado', 'rfc', 'motivo','puesto_funcional','nivel','unidad_administrativa')
    list_filter = (crear_filtro_conteo('motivo', 'Motivo'), crear_filtro_conteo('nivel', 'Nivel'), crear_filtro_conteo('unidad_administrativa', 'Unidad Administrativa'), crear_filtro_conteo('posicion', 'Posición'))
    fieldsets = (('Información del Empleado', {'fields': ('nombre', 'id_empleado', 'rfc', 'curp')}), ('Detalles de la Baja', {'fields': ('motivo', 'estado_nomina', 'fecha_efectiva_personal', 'fecha_de_captura')}), ('Información del Puesto', {'fields': ('posicion', 'puesto_funcional', 'unidad_administrativa')}), ('Fotografía', {'fields': ('mostrar_foto_de_base_de_datos',)}))
    readonly_fields = ('mostrar_foto_de_base_de_datos',)
    
    # --- MÉTODOS PARA FOTOS ---
    def mostrar_foto_de_base_de_datos(self, obj):
        if obj.foto:
            imagen_base64 = base64.b64encode(obj.foto).decode('utf-8')
            return format_html(f'<img src="data:image/jpeg;base64,{imagen_base64}" style="max-width: 200px; height: auto;" />')
        return "No hay imagen en la base de datos."
    mostrar_foto_de_base_de_datos.short_description = 'Fotografía'

    def mostrar_miniatura(self, obj):
        if obj.foto:
            imagen_base64 = base64.b64encode(obj.foto).decode('utf-8')
            return format_html(f'<img src="data:image/jpeg;base64,{imagen_base64}" style="width: 60px; height: auto;" />')
        return "N/A"
    mostrar_miniatura.short_description = 'Foto'

    # --- ACCIÓN DE EXPORTAR CON REGISTRO EN BITÁCORA ---
    @admin.action(description="Exportar Bajas seleccionadas a Excel con imágenes")
    def exportar_a_excel_con_imagenes(self, request, queryset):
        RegistroActividad.objects.create(usuario=request.user, tipo_accion='export', detalles=f"Exportó a Excel {queryset.count()} registros de Bajas de Personal.")
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "Bajas de Personal"
        headers = ['ID Empleado', 'Nombre', 'RFC', 'Posición', 'Motivo', 'Fecha Efectiva', 'Foto']
        sheet.append(headers)
        for registro in queryset:
            if registro.foto:
                try:
                    image_stream = BytesIO(registro.foto)
                    img = Image(image_stream)
                    proporcion = img.width / img.height
                    img.height = 80
                    img.width = 80 * proporcion
                except Exception: img = None
            else: img = None
            row_data = [registro.id_empleado, registro.nombre, registro.rfc, registro.posicion, registro.motivo, registro.fecha_efectiva_personal, '']
            sheet.append(row_data)
            if img:
                row_num = sheet.max_row
                sheet.add_image(img, f'G{row_num}')
                sheet.row_dimensions[row_num].height = 65
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="bajas_personal.xlsx"'
        workbook.save(response)
        return response

    # --- REGISTRO DE CONSULTAS Y BÚSQUEDAS ---
    def changelist_view(self, request, extra_context=None):
        search_term = request.GET.get('q', '')
        if search_term:
            log_user_view(request, f"Buscó '{search_term}' en Bajas de Personal.", include_filters=False)
        else:
            log_user_view(request, "Consultó la lista de Bajas de Personal.", include_filters=True)
        return super().changelist_view(request, extra_context)

    # --- REGISTRO DE VISTA DE DETALLE ---
    def change_view(self, request, object_id, form_url='', extra_context=None):
        try:
            obj = self.get_object(request, object_id)
            log_user_view(request, f"Consultó el detalle de Baja: {obj}", include_filters=False)
        except Exception:
            log_user_view(request, f"Intentó consultar detalle de Baja ID: {object_id}", include_filters=False)
        return super().change_view(request, object_id, form_url, extra_context)

    # --- GESTIÓN DE ACCIONES ---
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions: del actions['delete_selected']
        return actions

# Recuerda que tus modelos se registran en `core/admin_site.py`
