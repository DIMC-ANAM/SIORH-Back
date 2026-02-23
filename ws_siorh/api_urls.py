from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .api_views import BajasFinViewSet, PlantillaFinViewSet
from . import views

router = DefaultRouter()
router.register(r'plantillaFin', PlantillaFinViewSet, basename='plantilla-fin')
router.register(r'bajasFin', BajasFinViewSet, basename='bajas-fin')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/login/', views.auth_login, name='auth_login'),
    path('auth/me/', views.auth_me, name='auth_me'),
    path('plantilla/<str:posicion_pk>/pdf/', views.generar_cedula_pdf, name='generar_cedula_pdf'),
    path('plantilla/<str:posicion_pk>/detalle/', views.obtener_detalle_empleado, name='obtener_detalle_empleado'),
    path('baja/<str:pk>/pdf/', views.generar_baja_pdf, name='generar_baja_pdf'),
]
