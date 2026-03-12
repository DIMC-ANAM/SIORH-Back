from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone

from .models import RegistroActividad

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    ip = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')
    return ip

class ActivityLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        path = request.path or ''
        method = (request.method or 'GET').upper()

        # Auditar actividad del aplicativo (API), no navegación de Django Admin.
        if method == 'OPTIONS' or not path.startswith('/api/'):
            return response

        ignored_prefixes = (
            '/api/auth/login/',
            '/api/auth/me/',
            '/api/auditoria/registros/',
        )
        if any(path.startswith(prefix) for prefix in ignored_prefixes):
            return response

        user = request.user if getattr(request, 'user', None) and request.user.is_authenticated else None

        if user is None:
            user_id = (
                (request.headers.get('X-Usuario-Id') or '').strip()
                or str(request.GET.get('_uid') or '').strip()
            )
            if user_id.isdigit():
                try:
                    User = get_user_model()
                    user = User.objects.filter(id=int(user_id)).first()
                except Exception:
                    user = None

        if user is None:
            return response

        if '/pdf/' in path:
            tipo_accion = 'print'
        elif method == 'GET':
            tipo_accion = 'view'
        elif method == 'POST':
            tipo_accion = 'create'
        elif method in ('PUT', 'PATCH'):
            tipo_accion = 'update'
        elif method == 'DELETE':
            tipo_accion = 'delete'
        else:
            tipo_accion = 'view'

        query = request.META.get('QUERY_STRING', '')
        detalles = f"{method} {path}" + (f"?{query}" if query else '')

        try:
            last_seconds = timezone.now() - timedelta(seconds=20)
            ya_registrado = RegistroActividad.objects.filter(
                usuario=user,
                tipo_accion=tipo_accion,
                detalles=detalles,
                timestamp__gte=last_seconds,
            ).exists()

            if not ya_registrado:
                RegistroActividad.objects.create(
                    usuario=user,
                    tipo_accion=tipo_accion,
                    detalles=detalles,
                    ip_address=get_client_ip(request),
                )
        except Exception:
            # La auditoría no debe impedir la operación principal del API.
            return response
        
        return response