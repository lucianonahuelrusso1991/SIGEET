import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_escolar.settings')
django.setup()

from gestion.models import Alumno, Docente, Inscripcion, InscripcionMesa, MesaExamen, Comision, PlanDeEstudio, Comunicado, Notificacion, EventoInstitucional

def clean():
    print("Borrando datos transaccionales (alumnos, docentes, etc)...")
    Inscripcion.objects.all().delete()
    InscripcionMesa.objects.all().delete()
    MesaExamen.objects.all().delete()
    Comision.objects.all().delete()
    Alumno.objects.all().delete()
    Docente.objects.all().delete()
    Comunicado.objects.all().delete()
    Notificacion.objects.all().delete()
    EventoInstitucional.objects.all().delete()
    
    
    print("Borrando planes duplicados (3, 6, 7)...")
    PlanDeEstudio.objects.filter(id__in=[3, 6, 7]).delete()
    
    print("Base de datos limpia y reseteada. Quedan solo los planes:", [p.nombre for p in PlanDeEstudio.objects.all()])
    
if __name__ == '__main__':
    clean()
