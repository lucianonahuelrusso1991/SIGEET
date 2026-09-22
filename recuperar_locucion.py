import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sistema_escolar.settings")
django.setup()

from gestion.models import Alumno, PlanDeEstudio, Materia

def arreglar_materias_locucion():
    al = Alumno.objects.filter(dni='46027726').first() # Agustina Rivas
    plan_locucion = PlanDeEstudio.objects.filter(nombre__icontains='Locuci').filter(nombre__icontains='19').first()
    plan_hist = PlanDeEstudio.objects.filter(nombre__icontains='Hist').first()
    
    if not al or not plan_locucion or not plan_hist:
        print("Faltan datos base.")
        return
        
    # Recolectar todas las materias que Agustina Rivas tiene en su historia
    materias_agustina = set()
    for eq in al.equivalencias.all(): materias_agustina.add(eq.materia)
    for i in al.inscripciones.all(): materias_agustina.add(i.comision.materia)
    for m in al.mesas_inscriptas.all(): materias_agustina.add(m.mesa.materia)
    
    movidas = 0
    for m in materias_agustina:
        if m.plan == plan_hist:
            print(f"Recuperando: {m.nombre}")
            m.plan = plan_locucion
            m.save()
            movidas += 1
            
    print(f"Se recuperaron {movidas} materias perdidas al plan {plan_locucion.nombre}.")

arreglar_materias_locucion()