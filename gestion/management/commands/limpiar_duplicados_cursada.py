import os
from django.core.management.base import BaseCommand
from django.db import transaction

class Command(BaseCommand):
    help = 'Limpia comisiones "AN" duplicadas generadas por el primer script'

    def handle(self, *args, **options):
        from gestion.models import Comision, Inscripcion, Alumno, Materia, Nota
        
        duplicados_resueltos = 0
        comisiones_vaciadas = 0
        
        alumnos = Alumno.objects.all()
        for al in alumnos:
            inscripciones = Inscripcion.objects.filter(alumno=al).select_related('comision', 'comision__materia')
            
            agrupadas = {}
            for ins in inscripciones:
                key = (ins.comision.materia_id, ins.comision.ciclo_lectivo)
                if key not in agrupadas: agrupadas[key] = []
                agrupadas[key].append(ins)
                
            for key, lista_ins in agrupadas.items():
                if len(lista_ins) > 1:
                    buenas = []
                    malas = []
                    for ins in lista_ins:
                        tiene_notas = Nota.objects.filter(inscripcion=ins).exists()
                        if tiene_notas:
                            buenas.append(ins)
                        else:
                            if ins.comision.cuatrimestre == 'AN' and ins.comision.docente is None:
                                malas.append(ins)
                            else:
                                buenas.append(ins)
                                
                    if len(buenas) >= 1 and len(malas) >= 1:
                        for mala in malas:
                            com = mala.comision
                            mala.delete()
                            duplicados_resueltos += 1
                            if com.inscripciones.count() == 0:
                                com.delete()
                                comisiones_vaciadas += 1

        self.stdout.write(self.style.SUCCESS(f"Duplicados de cursada eliminados: {duplicados_resueltos}"))
        self.stdout.write(self.style.SUCCESS(f"Comisiones vacías eliminadas: {comisiones_vaciadas}"))