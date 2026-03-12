from django.contrib import admin
from .models import RegistroActividad

try:
    from core.admin_site import site as my_admin_site
except Exception:
    my_admin_site = admin.site

@admin.register(RegistroActividad, site=my_admin_site)
class RegistroActividadAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'usuario', 'tipo_accion', 'detalles', 'ip_address')
    list_filter = ('tipo_accion', 'usuario', 'timestamp')
    search_fields = ('usuario__username', 'detalles', 'ip_address')
    
    def has_add_permission(self, request): return False
    def has_change_permission(self, request, obj=None): return False
    def has_delete_permission(self, request, obj=None): return False