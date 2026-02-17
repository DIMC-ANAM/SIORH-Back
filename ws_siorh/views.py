# Añade estas importaciones al principio de tu archivo views.py
from django.contrib.staticfiles import finders
import base64
from django.contrib.staticfiles.storage import staticfiles_storage


# ... (el resto de tus importaciones) ...
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from weasyprint import HTML
from .models import PlantillaFin
from .models import BajasFin 
from auditoria.models import RegistroActividad # <-- IMPORTA


def generar_cedula_pdf(request, posicion_pk):
    try:
        obj = PlantillaFin.objects.get(pk=posicion_pk)
        RegistroActividad.objects.create(usuario=request.user, tipo_accion='print', detalles=f"Generó PDF de Cédula para: {obj}.")
    except Exception: pass
    # ... (resto de la vista)

#def generar_cedula_pdf(request, posicion_pk):
 #   """
  #  Genera un PDF para un registro específico de PlantillaFin.
   # """
    registro = get_object_or_404(PlantillaFin, pk=posicion_pk)

    # --- Lógica para la foto del empleado ---
    imagen_base64 = ""
    if registro.foto:
        imagen_base64 = base64.b64encode(registro.foto).decode('utf-8')

    # --- Lógica CORREGIDA para cargar el logo ---
    logo_base64 = ""
    # Usamos 'finders.find' que funciona tanto en local como en producción
    ruta_logo_origen = finders.find('core/img/logo.png')

    if ruta_logo_origen:
        try:
            with open(ruta_logo_origen, 'rb') as f:
                logo_data = f.read()
                logo_base64 = base64.b64encode(logo_data).decode('utf-8')
        except Exception as e:
            print(f"Error al leer el archivo del logo: {e}")
    else:
        print("ADVERTENCIA: El archivo 'core/img/logo.png' no fue encontrado por Django finders.")

    context = {
        'registro': registro,
        'imagen_base64': imagen_base64,
        'logo_base64': logo_base64,
    }

    # ... (el resto de la función que genera el PDF se queda igual)
    html_string = render_to_string('admin/cedula_template.html', context)
    pdf_file = HTML(string=html_string).write_pdf()
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="cedula_{registro.posicion}.pdf"'

    return response

def generar_baja_pdf(request, pk):
    try:
        obj = BajasFin.objects.get(pk=pk)
        RegistroActividad.objects.create(usuario=request.user, tipo_accion='print', detalles=f"Generó PDF de Baja para: {obj}.")
    except Exception: pass
    # ... (resto de la vista)
# --- NUEVA VISTA PARA EL REPORTE DE BAJA ---
#def generar_baja_pdf(request, pk):
    # 'pk' porque el modelo BajasFin usa el 'id' por defecto
    registro = get_object_or_404(BajasFin, pk=pk)

    imagen_base64 = ""
    if registro.foto:
        imagen_base64 = base64.b64encode(registro.foto).decode('utf-8')

    context = {
        'registro': registro,
        'imagen_base64': imagen_base64,
    }

    # Apuntamos al HTML 
    html_string = render_to_string('admin/baja_template.html', context)

    pdf_file = HTML(string=html_string).write_pdf()

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="reporte_baja_{registro.pk}.pdf"'

    return response