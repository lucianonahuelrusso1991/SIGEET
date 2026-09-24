from django.core.management.base import BaseCommand
from gestion.models import Materia, Inscripcion
from django.db.models import Q

class Command(BaseCommand):
    help = 'Aplica la resolucion oficial del plan de Locucion para materias con y sin final'

    def handle(self, *args, **kwargs):
        def normalize(n):
            return n.lower().strip().replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u').replace('ñ','n').replace(' ', '')
            
        finales_oficiales = [
            normalize('Argentina Contemporánea'),
            normalize('Ética Profesional'),
            normalize('Expresión Oral y Escrita'),
            normalize('Historia de la Cultura y el Arte'),
            normalize('Historia de la Cultura y Arte'),
            normalize('Legislación de Medios Audiovisuales'),
            normalize('Literatura'),
            normalize('Oratoria'),
            normalize('Problemática Religiosa Contemporánea'),
            normalize('Semiótica de los Medios Masivos'),
            normalize('Teorías de la Comunicación')
        ]
        
        promocionales_oficiales = [
            normalize('Técnicas de la Voz I'), normalize('Técnicas de la Voz II'), normalize('Técnicas de la Voz III'),
            normalize('Expresión Corporal'), normalize('Actuación Dramática'),
            normalize('Taller Integral de la Voz I'), normalize('Taller Integral de la Voz II'), normalize('Taller Integral de la Voz III'),
            normalize('Locución I'), normalize('Locución II'), normalize('Locución III'),
            normalize('Televisión I'), normalize('Televisión II'),
            normalize('Redacción Periodística'),
            normalize('Fonética Francesa'), normalize('Fonética Italiana'), normalize('Fonética Alemana'),
            normalize('Tecnología I'), normalize('Tecnología II'),
            normalize('Inglés'), normalize('Portugués'),
            normalize('Libretos y Guiones'),
            normalize('Doblaje'),
            normalize('Periodismo'),
            normalize('Práctica Profesionalizante en Radio I'), normalize('Práctica Profesionalizante en Radio II'), normalize('Práctica Profesionalizante en Radio III'),
            normalize('Práctica Profesionalizante en Conducción en Actos Públicos'),
            normalize('Práctica Profesionalizante en Televisión Integral'),
            normalize('Práctica Profesionalizante en Producción de Contenidos')
        ]
        
        materias = Materia.objects.all()
        modificadas_fin = 0
        modificadas_prom = 0
        
        for mat in materias:
            nombre_norm = normalize(mat.nombre)
            
            if nombre_norm in finales_oficiales:
                if mat.tipo_aprobacion != 'FIN':
                    mat.tipo_aprobacion = 'FIN'
                    mat.save(update_fields=['tipo_aprobacion'])
                    modificadas_fin += 1
            elif nombre_norm in promocionales_oficiales:
                if mat.tipo_aprobacion != 'PROM':
                    mat.tipo_aprobacion = 'PROM'
                    mat.save(update_fields=['tipo_aprobacion'])
                    modificadas_prom += 1
                    
        # Ahora que corregimos las materias, aseguramos que todas las inscripciones APR en PROM pasen a PROM
        inscripciones_a_corregir = Inscripcion.objects.filter(
            Q(estado='APR') | Q(estado='REG', comision__cerrada=True),
            Q(comision__materia__tipo_aprobacion='PROM')
        )
        
        corregidas_insc = 0
        for insc in inscripciones_a_corregir:
            insc.estado = 'PROM'
            insc.save(update_fields=['estado'])
            corregidas_insc += 1

        self.stdout.write(self.style.SUCCESS(f'Exito: {modificadas_fin} materias fijadas con FINAL. {modificadas_prom} materias fijadas como PROMOCIONALES. {corregidas_insc} alumnos actualizados.'))