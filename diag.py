import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sigeet.settings")
django.setup()

from gestion.models import Alumno, Materia, PlanDeEstudio, InscripcionCarrera

a = Alumno.objects.filter(dni='42649322').first()
if not a:
    print("No se encontro a Isabella")
else:
    print(f"Alumno: {a.nombre} {a.apellido}")
    print("Carreras inscriptas:")
    for ic in InscripcionCarrera.objects.filter(alumno=a):
        print(f" - {ic.plan.nombre} (Activo: {ic.plan.activo})")
        
    print("\nMaterias en plan Sistemas:")
    plan_sis = PlanDeEstudio.objects.filter(nombre__icontains='Sistemas').first()
    if plan_sis:
        print(f"Plan: {plan_sis.nombre}")
        for m in Materia.objects.filter(plan=plan_sis).order_by('nombre'):
            print(f"  - {m.nombre}")
    else:
        print("No se encontro plan sistemas")