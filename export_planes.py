import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_escolar.settings')
django.setup()

from gestion.models import PlanDeEstudio, Materia, Correlatividad

with open("load_online_planes.py", "w", encoding="utf-8") as f:
    f.write("import os\n")
    f.write("import django\n\n")
    f.write("os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_escolar.settings')\n")
    f.write("django.setup()\n\n")
    f.write("from gestion.models import PlanDeEstudio, Materia, Correlatividad\n\n")
    f.write("def run():\n")

    planes = PlanDeEstudio.objects.all()
    for p in planes:
        f.write(f"    plan_{p.id}, _ = PlanDeEstudio.objects.get_or_create(\n")
        f.write(f"        nombre={repr(p.nombre)},\n")
        f.write(f"        defaults={{'resolucion_ministerial': {repr(p.resolucion_ministerial)}}}\n")
        f.write(f"    )\n")
        f.write(f"    plan_{p.id}.resolucion_ministerial = {repr(p.resolucion_ministerial)}\n")
        f.write(f"    plan_{p.id}.save()\n\n")

    materias = Materia.objects.all()
    for m in materias:
        f.write(f"    mat_{m.id}, _ = Materia.objects.get_or_create(\n")
        f.write(f"        plan=plan_{m.plan.id},\n")
        f.write(f"        nombre={repr(m.nombre)},\n")
        f.write(f"        defaults={{\n")
        f.write(f"            'año_dictado': {repr(m.año_dictado)},\n")
        f.write(f"            'cuatrimestre_dictado': {repr(m.cuatrimestre_dictado)}\n")
        f.write(f"        }}\n")
        f.write(f"    )\n")
        f.write(f"    mat_{m.id}.año_dictado = {repr(m.año_dictado)}\n")
        f.write(f"    mat_{m.id}.cuatrimestre_dictado = {repr(m.cuatrimestre_dictado)}\n")
        f.write(f"    mat_{m.id}.save()\n\n")

    correlatividades = Correlatividad.objects.all()
    for c in correlatividades:
        f.write(f"    Correlatividad.objects.get_or_create(\n")
        f.write(f"        materia=mat_{c.materia.id},\n")
        f.write(f"        requisito=mat_{c.requisito.id},\n")
        f.write(f"        tipo={repr(c.tipo)}\n")
        f.write(f"    )\n")
        
    f.write("\n    print('¡Planes, materias y correlatividades sincronizados con exito!')\n\n")
    f.write("if __name__ == '__main__':\n")
    f.write("    run()\n")
