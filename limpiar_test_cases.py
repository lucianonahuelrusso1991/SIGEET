import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sistema_escolar.settings")
django.setup()

from gestion.models import Alumno, PlanDeEstudio, InscripcionCarrera

plan_historico = PlanDeEstudio.objects.filter(nombre__icontains='Hist').first()
test_cases = ['33774806', '44363997', '30149595', '46027726', '7766086', '42649322', '37687214', '39462473', '47130185']

borrados = 0
if plan_historico:
    for dni in test_cases:
        al = Alumno.objects.filter(dni=dni).first()
        if al:
            inscs = InscripcionCarrera.objects.filter(alumno=al, plan=plan_historico)
            if inscs.exists():
                inscs.delete()
                borrados += 1
                print(f"Limpiado Plan Historico de {al.nombre} {al.apellido}")

print(f"Total casos testigo limpiados: {borrados}")