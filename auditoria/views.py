from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_GET

from .models import RegistroActividad


@require_GET
def registros_actividad_api(request):
	"""Lista de registros de actividad para superusuarios."""
	user = getattr(request, 'user', None)
	es_superuser_autenticado = bool(user and user.is_authenticated and user.is_superuser)
	rol_front = str(request.GET.get('idUsuarioRol') or '').strip()

	# Si no hay sesión Django autenticada, se usa el rol enviado por frontend.
	if not es_superuser_autenticado and rol_front != '1':
		return JsonResponse({'status': 403, 'message': 'Acceso denegado.'}, status=403)

	page = max(int(request.GET.get('page', 1) or 1), 1)
	page_size = min(max(int(request.GET.get('page_size', 20) or 20), 1), 100)
	tipo = (request.GET.get('tipo') or '').strip()
	search = (request.GET.get('search') or '').strip()

	qs = RegistroActividad.objects.select_related('usuario').all().order_by('-timestamp')

	if tipo:
		qs = qs.filter(tipo_accion=tipo)

	if search:
		qs = qs.filter(
			Q(usuario__username__icontains=search)
			| Q(detalles__icontains=search)
			| Q(ip_address__icontains=search)
		)

	paginator = Paginator(qs, page_size)
	page_obj = paginator.get_page(page)

	results = [
		{
			'id': item.id,
			'timestamp': item.timestamp.isoformat() if item.timestamp else None,
			'usuario': item.usuario.username if item.usuario else 'Usuario eliminado',
			'tipo_accion': item.tipo_accion,
			'tipo_accion_display': item.get_tipo_accion_display(),
			'detalles': item.detalles or '',
			'ip_address': item.ip_address or '',
		}
		for item in page_obj.object_list
	]

	return JsonResponse(
		{
			'status': 200,
			'count': paginator.count,
			'page': page_obj.number,
			'total_pages': paginator.num_pages,
			'results': results,
		},
		status=200,
	)
