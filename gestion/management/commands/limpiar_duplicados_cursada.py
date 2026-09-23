import os
from django.core.management.base import BaseCommand
from django.db import transaction

class Command(BaseCommand):
    help = 'Limpia comisiones "AN" duplicadas generadas por el primer script'

    def handle(self, *args, **options):
        from gestion.models import Comision, Inscripcion, Alumno, Materia
        
        # Queremos buscar comisiones que son AN y no tienen docentes ni notas, pero el alumno tiene OTRA comision igual pero 1C/2C.
        # Más fácil: Buscar grupos de (Alumno, Materia, CicloLectivo) con > 1 Inscripcion.
        
        duplicados_resueltos = 0
        comisiones_vaciadas = 0
        
        alumnos = Alumno.objects.all()
        for al in alumnos:
            # Agrupar inscripciones por (materia, ciclo)
            inscripciones = Inscripcion.objects.filter(alumno=al).select_related('comision', 'comision__materia')
            
            # Map: (materia_id, ciclo_lectivo) -> list of Inscripcion
            agrupadas = {}
            for ins in inscripciones:
                key = (ins.comision.materia_id, ins.comision.ciclo_lectivo)
                if key not in agrupadas: agrupadas[key] = []
                agrupadas[key].append(ins)
                
            for key, lista_ins in agrupadas.items():
                if len(lista_ins) > 1:
                    # Hay duplicado!
                    # Identificar la "mala" (la que tiene cuatrimestre AN, docente None, y NO tiene Notas)
                    # O mas simple, la que no tiene ninguna Nota asociada
                    buenas = []
                    malas = []
                    for ins in lista_ins:
                        tiene_notas = ins.nota_set.exists()
                        if tiene_notas:
                            buenas.append(ins)
                        else:
                            # Si es AN y docente None, casi seguro es la mala
                            if ins.comision.cuatrimestre == 'AN' and ins.comision.docente is None:
                                malas.append(ins)
                            else:
                                buenas.append(ins)
                                
                    # Si pudimos separar
                    if len(buenas) >= 1 and len(malas) >= 1:
                        for mala in malas:
                            com = mala.comision
                            mala.delete()
                            duplicados_resueltos += 1
                            # Si la comision quedó vacia, la borramos
                            if com.inscripciones.count() == 0:
                                com.delete()
                                comisiones_vaciadas += 1

        self.stdout.write(self.style.SUCCESS(f"Duplicados de cursada eliminados: {duplicados_resueltos}"))
        self.stdout.write(self.style.SUCCESS(f"Comisiones vacías eliminadas: {comisiones_vaciadas}"))