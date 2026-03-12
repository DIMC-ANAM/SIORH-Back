# auditoria/utils.py

from .models import RegistroActividad
from django.utils import timezone
from datetime import timedelta

# ▼▼▼ MODIFICACIÓN EN LA DEFINICIÓN DE LA FUNCIÓN ▼▼▼
def log_user_view(request, details_base, include_filters=True): # <-- Añadimos el parámetro
    """
    Crea un registro de actividad de tipo 'view'.
    Si include_filters=True, añade los filtros de consulta.
    """
    if request.user.is_authenticated:
        
        final_details = details_base
        
        # ▼▼▼ LÓGICA DE FILTROS AHORA CONDICIONADA ▼▼▼
        # Solo añadimos filtros si se solicita explícitamente y no es una búsqueda ('q' no existe)
        if include_filters and not request.GET.get('q'): 
            query_params = request.GET.copy()
            params_a_ignorar = ['p', 'o', 'q'] # 'q' ya se verifica arriba
            for param in params_a_ignorar:
                if param in query_params:
                    del query_params[param]

            if query_params:
                filtros_str = ", ".join([f"{key}='{value}'" for key, value in query_params.items()])
                final_details += f" (Filtros: {filtros_str})"
        # ▲▲▲ FIN DE LA CONDICIÓN ▲▲▲

        # Lógica para no duplicar registros (sin cambios)
        last_minute = timezone.now() - timedelta(minutes=1)
        if not RegistroActividad.objects.filter(
            usuario=request.user,
            tipo_accion='view',
            detalles=final_details,
            timestamp__gte=last_minute
        ).exists():
            RegistroActividad.objects.create(
                usuario=request.user,
                tipo_accion='view',
                detalles=final_details
            )