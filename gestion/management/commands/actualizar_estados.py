from django.core.management.base import BaseCommand
from gestion.models import Alumno
from django.db import transaction

class Command(BaseCommand):
    help = 'Actualiza estados de alumnos a Egresado o Inactivo segn progreso y cursadas vigentes.'

    def handle(self, *args, **options):
        alumnos = Alumno.objects.all()
        
        egresados = 0
        inactivos = 0
        activos_recuperados = 0
        
        with transaction.atomic():
            for alumno in alumnos:
                es_egresado = False
                todas_eq = list(alumno.equivalencias.all())
                todas_prom = list(alumno.inscripciones.filter(estado='PROM').select_related('comision__materia'))
                todas_apr = list(alumno.mesas_inscriptas.filter(estado='APR').select_related('mesa__materia'))
                
                for plan in alumno.carreras.all():
                    total_materias = plan.materias.count()
                    if total_materias == 0:
                        continue
                        
                    materias_vistas = set()
                    
                    for eq in [e for e in todas_eq if e.materia.plan_id == plan.id]:
                        materias_vistas.add(eq.materia_id)
                        
                    for insc in [i for i in todas_prom if i.comision.materia.plan_id == plan.id]:
                        materias_vistas.add(insc.comision.materia_id)
                        
                    for mesa_insc in [m for m in todas_apr if m.mesa.materia.plan_id == plan.id]:
                        materias_vistas.add(mesa_insc.mesa.materia_id)
                        
                    if len(materias_vistas) >= total_materias:
                        es_egresado = True
                        break
                
                estado_anterior = alumno.estado_alumno
                
                if es_egresado:
                    if estado_anterior != 'EGR':
                        alumno.estado_alumno = 'EGR'
                        alumno.save(update_fields=['estado_alumno'])
                        egresados += 1
                else:
                    # Chequear cursada actual 2026 2C o AN
                    cursando_2026 = alumno.inscripciones.filter(
                        comision__ciclo_lectivo=2026,
                        comision__cuatrimestre__in=['2C', 'AN']
                    ).exists()
                    
                    if not cursando_2026:
                        # Si no cursa, inactivo (A menos que ya sea Inactivo)
                        if estado_anterior != 'INA':
                            alumno.estado_alumno = 'INA'
                            alumno.save(update_fields=['estado_alumno'])
                            inactivos += 1
                    else:
                        # Si EST curando, pero estaba INA, lo activamos? 
                        # El usuario no lo pidi explicitamente, pero es lgico.
                        # Mejor solo actualizar los que estaban INA y ahora cursan.
                        # Dejamos intactos COND_DOC y COND_PAG.
                        if estado_anterior == 'INA':
                            alumno.estado_alumno = 'ACT'
                            alumno.save(update_fields=['estado_alumno'])
                            activos_recuperados += 1

        self.stdout.write(self.style.SUCCESS(f'Proceso completado.'))
        self.stdout.write(f'- Nuevos Egresados (100% plan): {egresados}')
        self.stdout.write(f'- Pasados a Inactivos (No cursan 2C/AN 2026): {inactivos}')
        self.stdout.write(f'- Pasados a Activos (Cursaban pero estaban INA): {activos_recuperados}')
