import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sistema_escolar.settings")
django.setup()

from gestion.models import Materia, PlanDeEstudio

plan_sis = PlanDeEstudio.objects.filter(nombre__icontains='Sistemas').first()
plan_hist = PlanDeEstudio.objects.filter(nombre__icontains='Hist').first()

if plan_sis and plan_hist:
    # Materias que SI pertenecen a sistemas (agregadas por logica)
    validas_sistemas = [
        "Comunicación Visual",
        "Elementos de la Matemática",
        "Práctica Profesionalizante I: Producción Web",
        "Plataforma de Desarrollo",
        "Acreditación de Talleres, Jornadas o Seminarios de Actualización",
        "Seguridad e Integridad",
        "Ética y Deontología Profesional",
        "Modelos Estratégicos de Negocios",
        "Práctica Profesionalizante VI: Seminario Final",
        "Programación I",
        "Programación II",
        "Bases de Datos",
        "Ingeniería de Software",
        "Sistemas Operativos"
    ]
    
    movidas = 0
    for m in Materia.objects.filter(plan=plan_sis):
        es_valida = False
        for v in validas_sistemas:
            if v.lower() in m.nombre.lower():
                es_valida = True
                break
        
        if not es_valida:
            print(f"Moviendo '{m.nombre}' al plan Historico...")
            m.plan = plan_hist
            m.save()
            movidas += 1
            
    print(f"Se movieron {movidas} materias fuera de Sistemas.")