from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import RegistroActividad
from django.db.models.signals import post_save, post_delete
from django.contrib.admin.models import LogEntry

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    ip = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')
    return ip

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    RegistroActividad.objects.create(
        usuario=user, tipo_accion='login', ip_address=get_client_ip(request),
        detalles=f"Inicio de sesión exitoso."
    )

@receiver([post_save, post_delete])
def log_model_change(sender, instance, **kwargs):
    APPS_A_MONITOREAR = ['core', 'dashboard', 'auth']
    app_label, model_name = sender._meta.app_label, sender._meta.model_name
    
    if app_label not in APPS_A_MONITOREAR or model_name == 'registroactividad':
        return

    if kwargs.get('created', False): tipo_accion = 'create'
    elif 'created' in kwargs: tipo_accion = 'update'
    else: tipo_accion = 'delete'
        
    current_user = None
    try:
        latest_log = LogEntry.objects.filter(object_id=instance.pk).latest('action_time')
        current_user = latest_log.user
    except Exception:
        pass

    if current_user:
        RegistroActividad.objects.create(
            usuario=current_user, tipo_accion=tipo_accion,
            detalles=f"Objeto: {model_name.title()} '{str(instance)}' (ID: {instance.pk})"
        )