import base64
import json
import os
from decimal import Decimal
from pathlib import Path

from django.apps import apps as django_apps
from django.contrib.auth import authenticate
from django.contrib.staticfiles import finders
from django.contrib.staticfiles.storage import staticfiles_storage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from .models import BajasFin, PlantillaFin

try:
    from django.db.models.expressions import RawSQL
except Exception:
    RawSQL = None

try:
    from auditoria.models import RegistroActividad
except Exception:
    class _DummyRegistroManager:
        @staticmethod
        def create(*args, **kwargs):
            return None

    class RegistroActividad:
        objects = _DummyRegistroManager()


def formato_moneda(valor):
    if valor in (None, '', 0):
        return ''
    try:
        valor = Decimal(str(valor))
    except Exception:
        return str(valor)
    return f'${valor:,.2f}'


def _read_static_as_data_uri(static_path: str) -> str:
    try:
        with staticfiles_storage.open(static_path, 'rb') as file_handle:
            data = file_handle.read()
    except Exception:
        abs_path = finders.find(static_path)
        if not abs_path:
            return ''
        with open(abs_path, 'rb') as file_handle:
            data = file_handle.read()

    ext = static_path.split('.')[-1].lower()
    mime = 'image/png' if ext == 'png' else 'image/jpeg' if ext in ('jpg', 'jpeg', 'webp') else 'application/octet-stream'
    return f'data:{mime};base64,{base64.b64encode(data).decode("utf-8")}'


def _static_file_uri(static_path: str) -> str:
    abs_path = finders.find(static_path)
    if not abs_path:
        return ''
    return Path(abs_path).resolve().as_uri()


def _foto_empleado_base64(obj) -> str:
    for attr in ('foto', 'fotografia', 'imagen', 'foto_empleado', 'foto_binaria'):
        if not hasattr(obj, attr):
            continue

        val = getattr(obj, attr)
        if not val:
            continue

        if isinstance(val, (bytes, bytearray, memoryview)):
            raw = bytes(val)
            return 'data:image/jpeg;base64,' + base64.b64encode(raw).decode('utf-8')

        try:
            if hasattr(val, 'path'):
                with open(val.path, 'rb') as file_handle:
                    raw = file_handle.read()
                return 'data:image/jpeg;base64,' + base64.b64encode(raw).decode('utf-8')
        except Exception:
            continue

    return ''


def _get_model(model_name: str):
    for app_label in ('ws_siorh', 'core'):
        try:
            return django_apps.get_model(app_label, model_name)
        except Exception:
            continue
    return None


def _get_first_attr(obj, candidates):
    for name in candidates:
        if hasattr(obj, name):
            val = getattr(obj, name)
            if val not in (None, '', ' '):
                return str(val).strip()
    return ''


def _render_pdf(html_string: str, base_url: str) -> bytes:
    gtk_candidates = [
        r'C:\Program Files\GTK3-Runtime Win64\bin',
        r'C:\Program Files\GTK3-Runtime Win64\lib',
    ]
    for candidate in gtk_candidates:
        if os.path.isdir(candidate) and candidate.lower() not in os.environ.get('PATH', '').lower():
            os.environ['PATH'] = f'{candidate};{os.environ.get("PATH", "")}'

    try:
        from weasyprint import HTML
    except Exception as exc:
        raise RuntimeError(
            'No se encontró la dependencia weasyprint. '
            'Instala con: pip install weasyprint'
        ) from exc

    return HTML(string=html_string, base_url=base_url).write_pdf()


def obtener_detalle_empleado(request, posicion_pk):
    registro = get_object_or_404(PlantillaFin, pk=posicion_pk)

    num_empleado = _get_first_attr(registro, ['num_empleado', 'NUM_EMPLEADO'])

    historial_plaza = []
    movimientos_personal = []
    domicilio_data = {}

    mov_pos_model = _get_model('MovPos')
    if mov_pos_model:
        try:
            historial_qs = mov_pos_model.objects.filter(n_pos_actual=registro.posicion).order_by('-f_efva')
            historial_plaza = [
                {
                    'fecha_efectiva': mov.f_efva,
                    'fecha_captura': mov.fecha_captura,
                    'estado': mov.estado_psn,
                    'motivo': mov.motivo,
                    'descripcion': mov.descr,
                    'departamento': mov.departamento,
                    'area': mov.unidad_de_negocio,
                    'nivel': mov.nivel_ptal,
                    'puesto_funcional': mov.puesto,
                }
                for mov in historial_qs
            ]
        except Exception:
            historial_plaza = []

    movimiento_model = _get_model('Movimiento')
    if movimiento_model and num_empleado:
        try:
            mov_qs = movimiento_model.objects.filter(id_empl=str(num_empleado)).order_by('-fecha_efectiva', '-fecha_captura')
            movimientos_personal = [
                {
                    'fecha_efectiva': mov.fecha_efectiva,
                    'fecha_captura': mov.fecha_captura,
                    'accion': mov.accion_nombre,
                    'motivo': mov.motivo_nombre,
                    'estado_pago': mov.estado_pago,
                    'unidad': mov.descr_larga1,
                    'posicion': mov.posicion,
                    'nivel': mov.puesto_ptal,
                    'puesto': mov.descr_larga,
                    'secuencia': mov.sec,
                }
                for mov in mov_qs
            ]
        except Exception:
            movimientos_personal = []

    domicilio_model = _get_model('Domicilio')
    if domicilio_model and num_empleado and str(num_empleado).isdigit() and RawSQL:
        try:
            domicilio = (
                domicilio_model.objects
                .annotate(no_emp_num=RawSQL('NO_EMPLEADO*1', []))
                .filter(no_emp_num=int(num_empleado))
                .first()
            )
            if domicilio:
                domicilio_data = {
                    'telefono': domicilio.phone,
                    'correo': domicilio.email_addr,
                    'direccion': ' '.join(
                        str(x).strip() for x in [
                            domicilio.calle,
                            f'No. {domicilio.hr_numero_exterior}' if domicilio.hr_numero_exterior else '',
                            f'Int. {domicilio.hr_numero_interior}' if domicilio.hr_numero_interior else '',
                            domicilio.colonia,
                            domicilio.hr_municipio,
                            domicilio.estado,
                            domicilio.postal,
                        ] if x and str(x).strip()
                    ),
                }
        except Exception:
            domicilio_data = {}

    payload = {
        'informacion_personal': {
            'nombres': registro.nombres,
            'rfc': registro.rfc,
            'curp': registro.curp,
            'num_empleado': registro.num_empleado,
            'foto_base64': _foto_empleado_base64(registro),
            **domicilio_data,
        },
        'detalles_puesto': {
            'posicion': registro.posicion,
            'estado_nomina': registro.estado_nomina,
            'nivel': registro.nivel,
            'smn': formato_moneda(registro.smn),
            'codigo_presupuestal': registro.codigo_presupuestal,
            'nombre_puesto_funcional': registro.nombre_puesto_funcional,
            'tipo_de_contratacion': registro.tipo_de_contratacion,
        },
        'ubicacion_administrativa': {
            'dg_o_aduana_compactada': registro.dg_o_aduana_compactada,
            'unidad_administrativa': registro.unidad_administrativa,
            'departamento': registro.departamento,
            'tipo_de_personal_sedena_semar': registro.tipo_de_personal_sedena_semar,
            'rango': registro.rango,
        },
        'historico_plaza': historial_plaza,
        'historico_movimientos_personal': movimientos_personal,
        'control_asistencia': {
            'disponible': False,
            'mensaje': 'Sin fuente de datos de asistencia en este backend.',
            'registros': [],
        },
    }

    return JsonResponse(payload, safe=False)


def generar_cedula_pdf(request, posicion_pk):
    registro = get_object_or_404(PlantillaFin, pk=posicion_pk)

    try:
        RegistroActividad.objects.create(
            usuario=request.user if getattr(request, 'user', None) and request.user.is_authenticated else None,
            tipo_accion='GENERAR_CEDULA_PDF',
            descripcion=f'Generó cédula PDF para PlantillaFin pk={posicion_pk}',
            fecha=timezone.now(),
        )
    except Exception:
        pass

    marco_uri = _read_static_as_data_uri('img/cedula/marco_cedula.png')
    fondo_uri = _read_static_as_data_uri('img/cedula/fondo_cedula.png')
    logo_uri = _read_static_as_data_uri('img/cedula/logo_hacienda_anam.png')

    if not marco_uri:
        marco_uri = _read_static_as_data_uri('img/marco_cedula.png')
    if not fondo_uri:
        fondo_uri = _read_static_as_data_uri('img/fondo_cedula.png')
    if not logo_uri:
        logo_uri = _read_static_as_data_uri('img/logo_hacienda_anam.png')

    patria_font_uri = _static_file_uri('fonts/Patria-Regular.otf')
    noto_regular_uri = _static_file_uri('fonts/NotoSans-Regular.ttf')
    noto_bold_uri = _static_file_uri('fonts/NotoSans-Bold.ttf')

    if not patria_font_uri:
        patria_font_uri = _static_file_uri('fonts/Patria_Regular.otf')

    foto_uri = _foto_empleado_base64(registro)

    datos_familiares = []
    movimientos = []
    domicilio = None

    no_empleado = _get_first_attr(registro, ['num_empleado', 'NUM_EMPLEADO'])

    familiar_model = _get_model('Familiar')
    if familiar_model and no_empleado and no_empleado.isdigit() and RawSQL:
        try:
            familiares_qs = (
                familiar_model.objects
                .annotate(emplid_num=RawSQL('EMPLID*1', []))
                .filter(emplid_num=int(no_empleado))
                .order_by('parentesco', 'hr_nombre')
            )
            datos_familiares = list(
                familiares_qs.values(
                    'hr_nombre',
                    'last_name100',
                    'hr_secnd_last_name',
                    'hr_curp',
                    'parentesco',
                    'tel_particular',
                    'tel_celular',
                    'correo_electronico',
                    'mismo_domicilio',
                    'sexo',
                )
            )
        except Exception:
            datos_familiares = []

    movimiento_model = _get_model('Movimiento')
    if movimiento_model and no_empleado and no_empleado.isdigit() and RawSQL:
        try:
            movimientos_qs = (
                movimiento_model.objects
                .annotate(id_empl_num=RawSQL('Id_empl*1', []))
                .filter(id_empl_num=int(no_empleado))
                .order_by('-fecha_efectiva', '-fecha_captura', '-fh_ult_actz')
            )
            movimientos = list(movimientos_qs.values())
        except Exception:
            movimientos = []

    domicilio_model = _get_model('Domicilio')
    if domicilio_model and no_empleado and no_empleado.isdigit() and RawSQL:
        try:
            domicilio = (
                domicilio_model.objects
                .annotate(no_emp_num=RawSQL('NO_EMPLEADO*1', []))
                .filter(no_emp_num=int(no_empleado))
                .first()
            )
        except Exception:
            domicilio = None

    context = {
        'hoy': timezone.localtime(timezone.now()),
        'registro': registro,
        'marco_uri': marco_uri,
        'fondo_uri': fondo_uri,
        'logo_uri': logo_uri,
        'foto_uri': foto_uri,
        'patria_font_uri': patria_font_uri,
        'noto_regular_uri': noto_regular_uri,
        'noto_bold_uri': noto_bold_uri,
        'datos_familiares': datos_familiares,
        'domicilio': domicilio,
        'smb_fmt': formato_moneda(registro.smb),
        'smn_fmt': formato_moneda(registro.smn),
        'movimientos': movimientos,
        'experiencia_externa': [],
        'viajes_internacionales': [],
        'declaraciones_patrimoniales': [],
    }

    html_string = render_to_string('admin/cedula_template.html', context=context, request=request)
    try:
        pdf_bytes = _render_pdf(html_string, request.build_absolute_uri('/'))
    except RuntimeError as exc:
        return HttpResponse(str(exc), status=500, content_type='text/plain; charset=utf-8')

    num_empleado_archivo = _get_first_attr(registro, ['num_empleado', 'NUM_EMPLEADO']) or posicion_pk
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="cedula_{num_empleado_archivo}.pdf"'
    return response


def generar_baja_pdf(request, pk):
    registro = get_object_or_404(BajasFin, pk=pk)

    try:
        RegistroActividad.objects.create(
            usuario=request.user if getattr(request, 'user', None) and request.user.is_authenticated else None,
            tipo_accion='GENERAR_BAJA_PDF',
            descripcion=f'Generó baja PDF para BajasFin pk={pk}',
            fecha=timezone.now(),
        )
    except Exception:
        pass

    context = {
        'hoy': timezone.localtime(timezone.now()),
        'registro': registro,
        'imagen_base64': base64.b64encode(registro.foto).decode('utf-8') if registro.foto else '',
    }

    html_string = render_to_string('admin/baja_template.html', context)
    try:
        pdf_file = _render_pdf(html_string, request.build_absolute_uri('/'))
    except RuntimeError as exc:
        return HttpResponse(str(exc), status=500, content_type='text/plain; charset=utf-8')
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="reporte_baja_{registro.pk}.pdf"'
    return response


def _resolve_role_from_user(user):
    if user.is_superuser:
        return 1, 'Súper administrador'

    group_names = [g.name.strip() for g in user.groups.all() if g.name]
    normalized = [name.lower() for name in group_names]

    if any(any(key in name for key in ('super', 'root')) for name in normalized):
        return 1, group_names[0] if group_names else 'Súper administrador'

    if any('admin' in name for name in normalized):
        return 2, group_names[0] if group_names else 'Administrador'

    if any(any(key in name for key in ('captura', 'operador', 'movimiento')) for name in normalized):
        return 3, group_names[0] if group_names else 'Operador'

    if any(any(key in name for key in ('consulta', 'lector', 'viewer')) for name in normalized):
        return 4, group_names[0] if group_names else 'Consulta'

    if group_names:
        return 4, group_names[0]

    return 4, 'Usuario'


def _user_session_payload(user):
    full_name = user.get_full_name().strip() or user.username
    role_id, area_name = _resolve_role_from_user(user)
    permissions = sorted(list(user.get_all_permissions()))
    groups = sorted(list(user.groups.values_list('name', flat=True)))

    return {
        'nombreCompleto': full_name,
        'idUsuario': user.id,
        'unidadAdscripcion': '',
        'idDeterminante': 1,
        'idUsuarioRol': role_id,
        'area': area_name,
        'username': user.username,
        'email': user.email,
        'grupos': groups,
        'permisos': permissions,
        'is_superuser': user.is_superuser,
    }


@csrf_exempt
def auth_login(request):
    if request.method != 'POST':
        return JsonResponse({'status': 405, 'message': 'Método no permitido.'}, status=405)

    try:
        body = json.loads(request.body.decode('utf-8') or '{}')
    except Exception:
        body = {}

    username = (body.get('username') or body.get('usuario') or body.get('email') or '').strip()
    password = (body.get('password') or '').strip()

    if not username or not password:
        return JsonResponse({'status': 400, 'message': 'Usuario y contraseña son obligatorios.'}, status=400)

    user = authenticate(request, username=username, password=password)
    if user is None:
        return JsonResponse({'status': 401, 'message': 'Credenciales inválidas.'}, status=401)

    if not user.is_active:
        return JsonResponse({'status': 403, 'message': 'Usuario inactivo.'}, status=403)

    return JsonResponse(
        {
            'status': 200,
            'message': 'Login exitoso.',
            'model': _user_session_payload(user),
        },
        status=200,
    )


def auth_me(request):
    user = getattr(request, 'user', None)
    if not user or not user.is_authenticated:
        return JsonResponse({'status': 401, 'message': 'No autenticado.'}, status=401)

    return JsonResponse({'status': 200, 'model': _user_session_payload(user)}, status=200)