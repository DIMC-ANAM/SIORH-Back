from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .api_views import BajasFinViewSet, PlantillaFinViewSet

router = DefaultRouter()
router.register(r'plantillaFin', PlantillaFinViewSet, basename='plantilla-fin')
router.register(r'bajasFin', BajasFinViewSet, basename='bajas-fin')

urlpatterns = [
    path('', include(router.urls)),
]
