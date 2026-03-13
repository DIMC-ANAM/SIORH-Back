#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'siorh.settings')
django.setup()

from ws_siorh.models import Acceso2025, PlantillaFin

try:
    plantilla = PlantillaFin.objects.get(posicion='10300009')
    num_emp = str(plantilla.num_empleado).strip()
    print(f"Num empleado: {num_emp}")
    
    accesos = Acceso2025.objects.filter(empleado=num_emp)
    print(f"Total de accesos: {accesos.count()}")
    
    for acc in accesos[:3]:
        print(f"  - {acc.date_raw}")
    
except Exception as e:
    print(f"Error: {e}")
