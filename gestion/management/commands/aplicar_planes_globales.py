from django.core.management.base import BaseCommand
from gestion.models import Materia, PlanDeEstudio, Inscripcion
from django.db.models import Q

class Command(BaseCommand):
    help = 'Aplica las reglas globales de promocion para todas las carreras del Instituto'

    def handle(self, *args, **kwargs):
        def normalize(n):
            return n.lower().strip().replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u').replace('ñ','n').replace(' ', '')
            
        finales_locucion = [
            normalize('Argentina Contemporánea'), normalize('Ética Profesional'),
            normalize('Expresión Oral y Escrita'), normalize('Historia de la Cultura y el Arte'),
            normalize('Historia de la Cultura y Arte'), normalize('Legislación de Medios Audiovisuales'),
            normalize('Literatura'), normalize('Oratoria'),
            normalize('Problemática Religiosa Contemporánea'), normalize('Semiótica de los Medios Masivos'),
            normalize('Teorías de la Comunicación')
        ]
        
        planes = PlanDeEstudio.objects.all()
        modificadas = 0
        
        for plan in planes:
            nombre_plan = normalize(plan.nombre)
            
            for mat in plan.materias.all():
                nombre_mat = normalize(mat.nombre)
                nuevo_tipo = 'FIN'
                
                # REGLA 1: Sistemas (Todas FIN)
                if 'sistema' in nombre_plan:
                    nuevo_tipo = 'FIN'
                    
                # REGLA 2: Produccion de TV (Todas PROM)
                elif 'produccion' in nombre_plan or 'tv' in nombre_plan or 'television' in nombre_plan:
                    nuevo_tipo = 'PROM'
                    
                # REGLA 3: Locucion (Lista estricta)
                elif 'locucion' in nombre_plan:
                    if nombre_mat in finales_locucion:
                        nuevo_tipo = 'FIN'
                    else:
                        nuevo_tipo = 'PROM'
                        
                # REGLA 4: Ciencias Sagradas, Filosofia y el resto
                else:
                    # En los profesorados, los Talleres, Practicas y Residencias son promocionales
                    if any(k in nombre_mat for k in ['taller', 'practica', 'residencia']):
                        nuevo_tipo = 'PROM'
                    else:
                        nuevo_tipo = 'FIN'
                        
                if mat.tipo_aprobacion != nuevo_tipo:
                    mat.tipo_aprobacion = nuevo_tipo
                    mat.save(update_fields=['tipo_aprobacion'])
                    modificadas += 1
                    
        # Y actualizamos las inscripciones retroactivamente
        inscripciones_a_corregir = Inscripcion.objects.filter(
            Q(estado='APR') | Q(estado='REG', comision__cerrada=True),
            Q(comision__materia__tipo_aprobacion='PROM')
        )
        corregidas_insc = 0
        for insc in inscripciones_a_corregir:
            insc.estado = 'PROM'
            insc.save(update_fields=['estado'])
            corregidas_insc += 1

        self.stdout.write(self.style.SUCCESS(f'Exito: {modificadas} materias actualizadas en todos los planes. {corregidas_insc} actas de alumnos corregidas.'))