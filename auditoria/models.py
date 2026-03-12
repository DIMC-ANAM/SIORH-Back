from django.db import models
from django.conf import settings

class RegistroActividad(models.Model):
    TIPO_ACCION_CHOICES = [
        ('login', 'Inicio de Sesión'),
        ('view', 'Consulta de Vista'),
        ('create', 'Creación de Objeto'),
        ('update', 'Actualización de Objeto'),
        ('delete', 'Eliminación de Objeto'),
        ('export', 'Exportación de Datos'),
        ('print', 'Impresión de Documento'),
    ]
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name="Usuario")
    tipo_accion = models.CharField(max_length=10, choices=TIPO_ACCION_CHOICES, verbose_name="Tipo de Acción")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Fecha y Hora")
    detalles = models.TextField(blank=True, null=True, verbose_name="Detalles")
    ip_address = models.GenericIPAddressField(blank=True, null=True, verbose_name="Dirección IP")

    def __str__(self):
        user = self.usuario.username if self.usuario else "Usuario eliminado"
        return f"{user} - {self.get_tipo_accion_display()} - {self.timestamp.strftime('%d/%b/%Y %H:%M')}"

    class Meta:
        verbose_name = "Registro de Actividad"
        verbose_name_plural = "Registros de Actividad"
        ordering = ['-timestamp']